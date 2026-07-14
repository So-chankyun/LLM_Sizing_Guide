from fastapi import APIRouter
from app.domains.calculator.schemas import SpecListResponse
from configs.model_specs import MODEL_SPECS as default_models
from configs.gpu_specs import GPU_SPECS as default_gpus
from app.domains.calculator.models import ModelSpec, GPUSpec

router = APIRouter(prefix="/specs", tags=["specs"])

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

@router.get("/gpus", response_model=SpecListResponse)
def get_gpus():
    return SpecListResponse(gpus=[_to_pydantic_gpu(g) for g in default_gpus])

@router.get("/models", response_model=SpecListResponse)
def get_models():
    return SpecListResponse(models=[_to_pydantic_model(m) for m in default_models])
