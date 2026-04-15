import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import json
import asyncio

from main import app, gpu_monitor, sys_controller, scheduler

class TestMainAPI:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @patch.object(gpu_monitor, 'get_gpu_status')
    def test_health_check(self, mock_get_status, client):
        mock_get_status.return_value = None
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    @patch.object(scheduler, 'get_available_models')
    def test_list_models(self, mock_get_models, client):
        mock_get_models.return_value = ["gemma-2-9b", "llama-3-8b"]
        response = client.get("/v1/models")
        
        assert response.status_code == 200
        data = response.json()
        assert data["object"] == "list"
        assert len(data["data"]) == 2
        assert data["data"][0]["id"] == "gemma-2-9b"
        assert data["data"][1]["id"] == "llama-3-8b"

    @patch.object(scheduler, 'is_model_available')
    def test_chat_completions_model_not_found(self, mock_is_available, client):
        mock_is_available.return_value = False
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "unknown-model",
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @patch.object(scheduler, 'is_model_available')
    @patch.object(gpu_monitor, 'get_gpu_status')
    def test_chat_completions_insufficient_memory(self, mock_get_status, mock_is_available, client):
        mock_is_available.return_value = True
        mock_get_status.return_value = {
            "available_memory": 1 * 1024 ** 3  # 1GB < 2GB required
        }
        
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "gemma-2-9b",
                "messages": [{"role": "user", "content": "Hello"}]
            }
        )
        
        assert response.status_code == 503
        assert "Insufficient GPU memory" in response.json()["detail"]

    @patch.object(scheduler, 'is_model_available')
    @patch.object(gpu_monitor, 'get_gpu_status')
    @patch.object(scheduler, 'is_model_running')
    @patch.object(scheduler, 'start_model')
    @patch.object(scheduler, 'get_model_port')
    @patch('httpx.AsyncClient.post')
    def test_chat_completions_non_streaming(
        self, mock_post, mock_get_port, mock_start_model, 
        mock_is_running, mock_get_status, mock_is_available, client
    ):
        mock_is_available.return_value = True
        mock_get_status.return_value = {
            "available_memory": 10 * 1024 ** 3
        }
        mock_is_running.return_value = True
        mock_get_port.return_value = 8000
        
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "id": "test-id",
            "object": "chat.completion",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "Hi!"}}]
        }
        mock_post.return_value.__aenter__.return_value = Mock(post=Mock(return_value=mock_response))
        
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "gemma-2-9b",
                "messages": [{"role": "user", "content": "Hello"}],
                "stream": False
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["object"] == "chat.completion"
        assert len(data["choices"]) == 1

    @patch.object(scheduler, 'is_model_available')
    @patch.object(gpu_monitor, 'get_gpu_status')
    def test_get_gpu_status_unavailable(self, mock_get_status, mock_is_available, client):
        mock_get_status.return_value = None
        response = client.get("/manage/gpu")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "unavailable"

    @patch.object(scheduler, 'is_model_available')
    @patch.object(scheduler, 'is_model_running')
    @patch.object(scheduler, 'get_model_port')
    @patch.object(scheduler, 'get_model_service')
    def test_get_model_status(self, mock_get_service, mock_get_port, mock_is_running, mock_is_available, client):
        mock_is_available.return_value = True
        mock_is_running.return_value = True
        mock_get_port.return_value = 8000
        mock_get_service.return_value = "vllm-gemma"
        
        response = client.get("/manage/models")
        
        assert response.status_code == 200
        data = response.json()
        assert "gemma-2-9b" in data
        assert data["gemma-2-9b"]["running"] is True

    @patch.object(scheduler, 'is_model_available')
    @patch.object(scheduler, 'is_model_running')
    @patch.object(scheduler, 'start_model')
    def test_start_model_success(self, mock_start_model, mock_is_running, mock_is_available, client):
        mock_is_available.return_value = True
        mock_is_running.return_value = False
        mock_start_model.return_value = True
        
        response = client.post("/manage/models/gemma-2-9b/start")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "starting"
        assert data["model"] == "gemma-2-9b"

    @patch.object(scheduler, 'is_model_available')
    @patch.object(scheduler, 'is_model_running')
    def test_start_model_already_running(self, mock_is_running, mock_is_available, client):
        mock_is_available.return_value = True
        mock_is_running.return_value = True
        
        response = client.post("/manage/models/gemma-2-9b/start")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "already_running"

    @patch.object(scheduler, 'is_model_available')
    @patch.object(scheduler, 'is_model_running')
    @patch.object(scheduler, 'stop_model')
    def test_stop_model_success(self, mock_stop_model, mock_is_running, mock_is_available, client):
        mock_is_available.return_value = True
        mock_is_running.return_value = True
        mock_stop_model.return_value = True
        
        response = client.post("/manage/models/gemma-2-9b/stop")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "stopped"
        assert data["model"] == "gemma-2-9b"

    @patch.object(scheduler, 'is_model_available')
    def test_stop_model_not_found(self, mock_is_available, client):
        mock_is_available.return_value = False
        
        response = client.post("/manage/models/unknown/stop")
        
        assert response.status_code == 404