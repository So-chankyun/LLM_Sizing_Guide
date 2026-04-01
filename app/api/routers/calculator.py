from fastapi import APIRouter, Depends
from typing import List
from app.api import deps
from app.domains.calculator.schemas import (
    CalculationRequest,
    MemoryFootprintResponse,
    PerformanceResponse
)
from app.domains.calculator.service import CalculatorService
from configs.model_specs import MODEL_SPECS as default_models
from configs.gpu_specs import GPU_SPECS as default_gpus
from app.domains.calculator.models import ModelSpec, GPUSpec

router = APIRouter(prefix="/calculate", tags=["calculate"])

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

@router.post("/memory", response_model=MemoryFootprintResponse)
def calculate_memory(
    request: CalculationRequest,
):
    service = CalculatorService(num_gpu=request.num_gpu)
    
    models = request.custom_models if request.custom_models else [_to_pydantic_model(m) for m in default_models]
    
    results = service.evaluate_memory_footprint(
        models=models,
        prompt_size=request.prompt_size,
        response_size=request.response_size,
        n_concurrent_request=request.n_concurrent_request
    )
    return MemoryFootprintResponse(results=results)

@router.post("/performance", response_model=PerformanceResponse)
def calculate_performance(
    request: CalculationRequest,
):
    service = CalculatorService(num_gpu=request.num_gpu)
    
    models = request.custom_models if request.custom_models else [_to_pydantic_model(m) for m in default_models]
    gpus = request.custom_gpus if request.custom_gpus else [_to_pydantic_gpu(g) for g in default_gpus]
    
    results = service.evaluate_performance(
        models=models,
        gpus=gpus,
        prompt_size=request.prompt_size,
        response_size=request.response_size,
        n_concurrent_request=request.n_concurrent_request
    )
    return PerformanceResponse(results=results)
