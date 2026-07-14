from app.domains.calculator.service import CalculatorService
from app.domains.calculator.models import ModelSpec, GPUSpec
from configs.model_specs import MODEL_SPECS
from configs.gpu_specs import GPU_SPECS

def _to_pydantic_model(m) -> ModelSpec:
    return ModelSpec(
        name=m.name,
        params_billion=m.params_billion,
        d_model=m.d_model,
        n_heads=m.n_heads,
        n_kv_heads=m.n_kv_heads,
        n_layers=m.n_layers,
        max_context_window=m.max_context_window
    )

def _to_pydantic_gpu(g) -> GPUSpec:
    return GPUSpec(
        name=g.name,
        fp16_tflops=g.fp16_tflops,
        memory_gb=g.memory_gb,
        memory_bandwidth_gbps=g.memory_bandwidth_gbps
    )

def test_memory_footprint_evaluation():
    service = CalculatorService(num_gpu=1)
    models = [_to_pydantic_model(m) for m in MODEL_SPECS]
    results = service.evaluate_memory_footprint(models, prompt_size=4096, response_size=256, n_concurrent_request=10)
    
    assert len(results) == len(models)
    assert results[0].input_size_tokens == 4096
    assert results[0].memory_footprint_gb > 0

def test_performance_evaluation():
    service = CalculatorService(num_gpu=1)
    models = [_to_pydantic_model(m) for m in MODEL_SPECS]
    gpus = [_to_pydantic_gpu(g) for g in GPU_SPECS]
    
    results = service.evaluate_performance(models, gpus, prompt_size=4096, response_size=256, n_concurrent_request=10)
    
    assert len(results) == len(models) * len(gpus)
    assert "kv_cache_tokens" in results[0].performance.model_dump()
