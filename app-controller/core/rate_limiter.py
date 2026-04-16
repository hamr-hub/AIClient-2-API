import redis
import os
import json
import uuid
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self):
        self.redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
        self.client = self._connect()
        self.prefix = "ai_controller:"
        self.queue_prefix = f"{self.prefix}queue:"
        self.request_prefix = f"{self.prefix}request:"
        self.max_queue_length = 100
        self.queue_poll_interval = 0.5
    
    def _connect(self) -> redis.Redis:
        try:
            r = redis.from_url(self.redis_url)
            r.ping()
            return r
        except:
            return None
    
    def _get_active_key(self, model_name: str) -> str:
        return f"{self.prefix}active_requests:{model_name}"
    
    def _get_queue_key(self, model_name: str) -> str:
        return f"{self.queue_prefix}{model_name}"
    
    def _get_request_key(self, request_id: str) -> str:
        return f"{self.request_prefix}{request_id}"
    
    def increment_request(self, model_name: str) -> int:
        if not self.client:
            return 0
        key = self._get_active_key(model_name)
        return self.client.incr(key)
    
    def decrement_request(self, model_name: str) -> int:
        if not self.client:
            return 0
        key = self._get_active_key(model_name)
        value = self.client.decr(key)
        if value < 0:
            self.client.set(key, 0)
            return 0
        return value
    
    def get_active_requests(self, model_name: str) -> int:
        if not self.client:
            return 0
        key = self._get_active_key(model_name)
        value = self.client.get(key)
        return int(value) if value else 0
    
    def is_available(self, model_name: str, max_concurrent: int) -> bool:
        active = self.get_active_requests(model_name)
        return active < max_concurrent
    
    def reset_counter(self, model_name: str):
        if not self.client:
            return
        key = self._get_active_key(model_name)
        self.client.delete(key)
    
    def enqueue_request(self, model_name: str, request_data: Dict[str, Any]) -> str:
        if not self.client:
            return ""
        
        request_id = str(uuid.uuid4())
        queue_key = self._get_queue_key(model_name)
        request_key = self._get_request_key(request_id)
        
        request_info = {
            "id": request_id,
            "model_name": model_name,
            "data": request_data,
            "enqueued_at": datetime.now().isoformat(),
            "status": "queued"
        }
        
        self.client.set(request_key, json.dumps(request_info), ex=3600)
        self.client.rpush(queue_key, request_id)
        
        return request_id
    
    def dequeue_request(self, model_name: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            return None
        
        queue_key = self._get_queue_key(model_name)
        request_id = self.client.lpop(queue_key)
        
        if not request_id:
            return None
        
        request_key = self._get_request_key(request_id.decode())
        request_data = self.client.get(request_key)
        
        if request_data:
            info = json.loads(request_data)
            info["status"] = "processing"
            self.client.set(request_key, json.dumps(info), ex=3600)
            return info
        
        return None
    
    def get_queue_length(self, model_name: str) -> int:
        if not self.client:
            return 0
        
        queue_key = self._get_queue_key(model_name)
        return self.client.llen(queue_key)
    
    def get_queue_status(self, model_name: str) -> Dict[str, Any]:
        return {
            "active_requests": self.get_active_requests(model_name),
            "queue_length": self.get_queue_length(model_name)
        }
    
    def cancel_request(self, request_id: str) -> bool:
        if not self.client:
            return False
        
        request_key = self._get_request_key(request_id)
        request_data = self.client.get(request_key)
        
        if not request_data:
            return False
        
        info = json.loads(request_data)
        if info["status"] == "queued":
            model_name = info["model_name"]
            queue_key = self._get_queue_key(model_name)
            self.client.lrem(queue_key, 0, request_id)
        
        info["status"] = "cancelled"
        self.client.set(request_key, json.dumps(info), ex=60)
        
        return True
    
    def set_request_complete(self, request_id: str, result: Optional[Dict[str, Any]] = None):
        if not self.client:
            return
        
        request_key = self._get_request_key(request_id)
        request_data = self.client.get(request_key)
        
        if request_data:
            info = json.loads(request_data)
            info["status"] = "completed"
            info["completed_at"] = datetime.now().isoformat()
            if result:
                info["result"] = result
            self.client.set(request_key, json.dumps(info), ex=60)
    
    def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            return None
        
        request_key = self._get_request_key(request_id)
        request_data = self.client.get(request_key)
        
        if request_data:
            return json.loads(request_data)
        
        return None
    
    def get_all_queue_status(self) -> Dict[str, Dict[str, int]]:
        if not self.client:
            return {}
        
        pattern = f"{self.queue_prefix}*"
        keys = self.client.keys(pattern)
        
        status = {}
        for key in keys:
            model_name = key.decode().replace(self.queue_prefix, "")
            status[model_name] = {
                "active_requests": self.get_active_requests(model_name),
                "queue_length": self.get_queue_length(model_name)
            }
        
        return status
    
    def clear_queue(self, model_name: str):
        if not self.client:
            return
        
        queue_key = self._get_queue_key(model_name)
        self.client.delete(queue_key)
    
    def close(self):
        if self.client:
            self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()