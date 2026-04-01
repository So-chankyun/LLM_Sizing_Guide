def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_gpus(client):
    response = client.get("/api/v1/specs/gpus")
    assert response.status_code == 200
    data = response.json()
    assert "gpus" in data
    assert len(data["gpus"]) > 0

def test_get_models(client):
    response = client.get("/api/v1/specs/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0

def test_calculate_memory(client):
    payload = {
        "num_gpu": 1,
        "prompt_size": 1024,
        "response_size": 128,
        "n_concurrent_request": 5
    }
    response = client.post("/api/v1/calculate/memory", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0

def test_calculate_performance(client):
    payload = {
        "num_gpu": 2,
        "prompt_size": 2048,
        "response_size": 256,
        "n_concurrent_request": 10
    }
    response = client.post("/api/v1/calculate/performance", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0
