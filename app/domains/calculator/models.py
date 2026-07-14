from typing import Union, Optional
from pydantic import BaseModel, Field

class GPUSpec(BaseModel):
    name: str
    fp16_tflops: float
    memory_gb: int
    memory_bandwidth_gbps: int

class ModelSpec(BaseModel):
    name: str
    params_billion: float
    d_model: int
    n_heads: int
    n_kv_heads: int
    n_layers: int
    max_context_window: int

class PerformanceMetrics(BaseModel):
    kv_cache_tokens: int
    prefill_time_per_token: Union[float, str]
    tpot: Union[float, str]
    ttft: Union[float, str]
    e2e_latency: Union[float, str]
    throughput: Union[float, str]
