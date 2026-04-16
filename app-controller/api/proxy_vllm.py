import httpx
import json
import asyncio
import os
from typing import Dict, Any, Optional

class VLLMProxy:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(60))
        self._last_flush_time = 0
        self._flush_interval = 300
    
    async def chat_completion(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/chat/completions"
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    async def chat_completion_stream(self, payload: Dict[str, Any]):
        url = f"{self.base_url}/v1/chat/completions"
        async with self.client.stream('POST', url, json=payload) as response:
            async for chunk in response.aiter_lines():
                if chunk.startswith("data: "):
                    chunk_data = chunk[6:]
                    if chunk_data == "[DONE]":
                        yield {
                            "id": f"chatcmpl-{os.urandom(12).hex()}",
                            "object": "chat.completion.chunk",
                            "created": int(asyncio.get_event_loop().time()),
                            "model": payload.get("model", ""),
                            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}]
                        }
                        break
                    try:
                        yield json.loads(chunk_data)
                    except json.JSONDecodeError:
                        continue
    
    async def list_models(self) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/models"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    async def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/v1/models/{model_name}"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None
    
    async def get_server_status(self) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/v1/server/status"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None
    
    async def flush_cache(self, force: bool = False) -> bool:
        current_time = asyncio.get_event_loop().time()
        if not force and (current_time - self._last_flush_time) < self._flush_interval:
            return False
        
        url = f"{self.base_url}/v1/flush"
        try:
            response = await self.client.post(url)
            response.raise_for_status()
            self._last_flush_time = current_time
            return True
        except httpx.HTTPError:
            return False
    
    async def set_gpu_memory_utilization(self, utilization: float) -> bool:
        url = f"{self.base_url}/v1/config/gpu_memory_utilization"
        try:
            response = await self.client.post(url, json={"gpu_memory_utilization": utilization})
            response.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
    
    async def get_gpu_memory_utilization(self) -> Optional[float]:
        url = f"{self.base_url}/v1/config/gpu_memory_utilization"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("gpu_memory_utilization")
        except httpx.HTTPError:
            return None
    
    async def optimize_memory(self, strategy: str = "aggressive") -> Dict[str, Any]:
        result = {
            "flush_cache": False,
            "memory_utilization_set": False,
            "utilization_value": None
        }
        
        result["flush_cache"] = await self.flush_cache(force=True)
        
        if strategy == "conservative":
            utilization = 0.8
        elif strategy == "balanced":
            utilization = 0.9
        elif strategy == "aggressive":
            utilization = 0.95
        else:
            utilization = 0.9
        
        result["memory_utilization_set"] = await self.set_gpu_memory_utilization(utilization)
        result["utilization_value"] = utilization
        
        return result
    
    async def get_model_stats(self, model_name: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/v1/models/{model_name}/stats"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            return None
    
    async def close(self):
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self.close()