from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
from core.logger import setup_logger
from core.redis_client import redis_client

logger = setup_logger()

class MetricsCollector:
    def __init__(self):
        self.request_counts: Dict[str, int] = defaultdict(int)
        self.error_counts: Dict[str, int] = defaultdict(int)
        self.response_times: List[float] = []
        self.model_requests: Dict[str, int] = defaultdict(int)
        self.start_time = datetime.now()
        self.gpu_status_history: List[Dict] = []
        self.queue_length_history: List[int] = []
        self.redis_prefix = "ai_controller:metrics:"
        self._load_from_redis()
    
    def _get_key(self, name: str) -> str:
        return f"{self.redis_prefix}{name}"
    
    def _load_from_redis(self):
        if not redis_client.is_connected():
            return
        
        try:
            request_counts_key = self._get_key("request_counts")
            data = redis_client.get_json(request_counts_key)
            if data:
                self.request_counts = defaultdict(int, data)
            
            error_counts_key = self._get_key("error_counts")
            data = redis_client.get_json(error_counts_key)
            if data:
                self.error_counts = defaultdict(int, data)
            
            model_requests_key = self._get_key("model_requests")
            data = redis_client.get_json(model_requests_key)
            if data:
                self.model_requests = defaultdict(int, data)
            
            response_times_key = self._get_key("response_times")
            data = redis_client.get_json(response_times_key)
            if data:
                self.response_times = data
            
            start_time_key = self._get_key("start_time")
            data = redis_client.get(start_time_key)
            if data:
                try:
                    self.start_time = datetime.fromisoformat(data)
                except:
                    pass
        except Exception as e:
            logger.error(f"Failed to load metrics from Redis: {e}")
    
    def _save_to_redis(self):
        if not redis_client.is_connected():
            return
        
        try:
            request_counts_key = self._get_key("request_counts")
            redis_client.set_json(request_counts_key, dict(self.request_counts))
            
            error_counts_key = self._get_key("error_counts")
            redis_client.set_json(error_counts_key, dict(self.error_counts))
            
            model_requests_key = self._get_key("model_requests")
            redis_client.set_json(model_requests_key, dict(self.model_requests))
            
            response_times_key = self._get_key("response_times")
            redis_client.set_json(response_times_key, self.response_times)
            
            start_time_key = self._get_key("start_time")
            redis_client.set(start_time_key, self.start_time.isoformat())
        except Exception as e:
            logger.error(f"Failed to save metrics to Redis: {e}")
    
    def record_request(self, endpoint: str, status_code: int, response_time: float, model_name: Optional[str] = None):
        self.request_counts[endpoint] += 1
        
        if status_code >= 400:
            self.error_counts[endpoint] += 1
        
        self.response_times.append(response_time)
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        
        if model_name:
            self.model_requests[model_name] += 1
        
        self._save_to_redis()
    
    def record_gpu_status(self, gpu_status: Dict):
        self.gpu_status_history.append({
            "timestamp": datetime.now().isoformat(),
            **gpu_status
        })
        if len(self.gpu_status_history) > 60:
            self.gpu_status_history = self.gpu_status_history[-60:]
        
        gpu_history_key = self._get_key("gpu_history")
        redis_client.set_json(gpu_history_key, self.gpu_status_history)
    
    def record_queue_length(self, length: int):
        self.queue_length_history.append(length)
        if len(self.queue_length_history) > 60:
            self.queue_length_history = self.queue_length_history[-60:]
        
        queue_history_key = self._get_key("queue_history")
        redis_client.set_json(queue_history_key, self.queue_length_history)
    
    def get_metrics(self) -> Dict:
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        max_response_time = max(self.response_times) if self.response_times else 0
        min_response_time = min(self.response_times) if self.response_times else 0
        
        uptime = datetime.now() - self.start_time
        
        avg_queue_length = sum(self.queue_length_history) / len(self.queue_length_history) if self.queue_length_history else 0
        max_queue_length = max(self.queue_length_history) if self.queue_length_history else 0
        
        return {
            "uptime": str(uptime),
            "total_requests": sum(self.request_counts.values()),
            "total_errors": sum(self.error_counts.values()),
            "request_counts": dict(self.request_counts),
            "error_counts": dict(self.error_counts),
            "response_time": {
                "average": round(avg_response_time, 2),
                "max": round(max_response_time, 2),
                "min": round(min_response_time, 2),
                "count": len(self.response_times)
            },
            "model_requests": dict(self.model_requests),
            "queue": {
                "average_length": round(avg_queue_length, 2),
                "max_length": max_queue_length,
                "history_length": len(self.queue_length_history)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_detailed_metrics(self) -> Dict:
        metrics = self.get_metrics()
        metrics["gpu_history"] = self.gpu_status_history
        return metrics
    
    def reset(self):
        self.request_counts.clear()
        self.error_counts.clear()
        self.response_times.clear()
        self.model_requests.clear()
        self.start_time = datetime.now()
        self.gpu_status_history.clear()
        self.queue_length_history.clear()
        
        if redis_client.is_connected():
            try:
                pattern = f"{self.redis_prefix}*"
                keys = redis_client.keys(pattern)
                for key in keys:
                    redis_client.delete(key)
            except Exception as e:
                logger.error(f"Failed to reset metrics in Redis: {e}")
    
    def get_health_score(self) -> float:
        total = sum(self.request_counts.values())
        errors = sum(self.error_counts.values())
        
        if total == 0:
            return 100.0
        
        error_rate = errors / total
        score = max(0, 100 - (error_rate * 100))
        return round(score, 2)
    
    def get_comprehensive_health_score(self, gpu_status: Optional[Dict] = None) -> Dict:
        scores = {}
        
        total = sum(self.request_counts.values())
        errors = sum(self.error_counts.values())
        
        if total > 0:
            error_rate = errors / total
            service_score = max(0, 100 - (error_rate * 100))
        else:
            service_score = 100.0
        
        scores["service"] = round(service_score, 2)
        
        if gpu_status and gpu_status.get("status") == "available":
            primary = gpu_status.get("primary", {})
            temp = primary.get("temperature", 0)
            total_mem = primary.get("total_memory", 1)
            used_mem = primary.get("used_memory", 0)
            
            temp_score = min(100, max(0, 100 - (temp - 85) * 2))
            mem_score = min(100, max(0, 100 - ((used_mem / total_mem) - 0.9) * 1000))
            
            scores["gpu_temperature"] = round(temp_score, 2)
            scores["gpu_memory"] = round(mem_score, 2)
            scores["gpu_overall"] = round((temp_score * 0.5 + mem_score * 0.5), 2)
        else:
            scores["gpu_temperature"] = 0.0
            scores["gpu_memory"] = 0.0
            scores["gpu_overall"] = 0.0
        
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        response_score = min(100, max(0, 100 - avg_response_time * 10))
        scores["response_time"] = round(response_score, 2)
        
        weights = {
            "service": 0.4,
            "gpu_overall": 0.3,
            "response_time": 0.3
        }
        
        overall_score = sum(scores.get(k, 0) * v for k, v in weights.items())
        scores["overall"] = round(overall_score, 2)
        
        scores["status"] = self._get_health_status(overall_score)
        
        return scores
    
    def _get_health_status(self, score: float) -> str:
        if score >= 90:
            return "healthy"
        elif score >= 70:
            return "degraded"
        elif score >= 50:
            return "warning"
        else:
            return "critical"
    
    def should_alert(self, threshold: float = 70) -> bool:
        score = self.get_health_score()
        return score < threshold
    
    def get_alert_reasons(self) -> List[str]:
        reasons = []
        
        total = sum(self.request_counts.values())
        errors = sum(self.error_counts.values())
        
        if total > 0:
            error_rate = errors / total
            if error_rate > 0.1:
                reasons.append(f"高错误率: {error_rate:.2%}")
        
        avg_response_time = sum(self.response_times) / len(self.response_times) if self.response_times else 0
        if avg_response_time > 5:
            reasons.append(f"响应时间过长: {avg_response_time:.2f}s")
        
        return reasons