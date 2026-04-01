from typing import List, Optional
from pydantic import BaseModel, Field
from app.domains.calculator.models import GPUSpec, ModelSpec, PerformanceMetrics

class CalculationRequest(BaseModel):
    num_gpu: int = Field(default=1, ge=1, description="Number of GPUs")
    prompt_size: int = Field(default=4096, ge=1, description="Prompt size in tokens")
    response_size: int = Field(default=256, ge=1, description="Response size in tokens")
    n_concurrent_request: int = Field(default=10, ge=1, description="Number of concurrent requests")
    
    # Optionally accept custom specs. If null, we use server's static specs.
    custom_gpus: Optional[List[GPUSpec]] = None
    custom_models: Optional[List[ModelSpec]] = None

class MemoryFootprintRow(BaseModel):
    model: str
    input_size_tokens: int
    output_size_tokens: int
    concurrent_requests: int
    kv_cache_size_per_token_gib: float
    memory_footprint_gb: float

class MemoryFootprintResponse(BaseModel):
    results: List[MemoryFootprintRow]

class PerformanceRow(BaseModel):
    model: str
    gpu: str
    gpu_count: float
    input_size_tokens: int
    output_size_tokens: int
    concurrent_requests: int
    performance: PerformanceMetrics

class PerformanceResponse(BaseModel):
    results: List[PerformanceRow]

class SpecListResponse(BaseModel):
    gpus: Optional[List[GPUSpec]] = None
    models: Optional[List[ModelSpec]] = None
