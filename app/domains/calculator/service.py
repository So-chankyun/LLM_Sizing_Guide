from typing import List, Optional
from app.domains.calculator.models import GPUSpec, ModelSpec, PerformanceMetrics
from app.domains.calculator.schemas import MemoryFootprintRow, PerformanceRow
from app.core.exceptions import OOMError

BYTES_IN_GiB = 1_073_741_824

class CalculatorService:
    def __init__(self, num_gpu: int):
        self.num_gpu = num_gpu

    def calc_kv_cache_size_per_token(self, model: ModelSpec) -> float:
        """Calculate KV cache size per token in GiB."""
        d_head = model.d_model / model.n_heads
        bytes_per_value = 2  # FP16 = 2 bytes
        return 2 * model.n_layers * model.n_kv_heads * d_head * bytes_per_value / BYTES_IN_GiB

    def calc_memory_footprint(self, model: ModelSpec, n_concurrent_request: int, context_window: int) -> float:
        """Calculate total memory footprint in GB."""
        kv_cache_size_per_token = self.calc_kv_cache_size_per_token(model)
        return (kv_cache_size_per_token * context_window * n_concurrent_request + 
                model.params_billion * 2)

    def calc_kv_cache_tokens(self, gpu: GPUSpec, model: ModelSpec, kv_cache_size: float) -> float:
        """Calculate maximum number of tokens that can fit in KV cache."""
        result = (self.num_gpu * gpu.memory_gb - 2 * model.params_billion) / kv_cache_size
        return max(0, result)

    def calc_prefill_time_per_token(self, model: ModelSpec, gpu: GPUSpec) -> float | str:
        """Calculate prefill time per token in milliseconds."""
        result = (2 * model.params_billion / self.num_gpu) / gpu.fp16_tflops
        return result if result >= 0 else "OOM"

    def calc_tpot(self, model: ModelSpec, gpu: GPUSpec) -> float | str:
        """Calculate token processing time (TPOT) in milliseconds."""
        result = (2 * model.params_billion / self.num_gpu) / gpu.memory_bandwidth_gbps * 1000
        return result if result >= 0 else "OOM"

    def calc_e2e_latency(self, prefill_time_per_token: float, tpot: float, prompt_size: int, response_size: int) -> float:
        """Calculate end-to-end latency in seconds."""
        return (prompt_size * prefill_time_per_token + response_size * tpot) / 1000

    def calculate_metrics(self, model: ModelSpec, gpu: GPUSpec, prompt_size: int, response_size: int) -> PerformanceMetrics:
        """Calculate all performance metrics for given model and GPU configuration."""
        kv_cache_size_per_token = self.calc_kv_cache_size_per_token(model)
        kv_cache_tokens = self.calc_kv_cache_tokens(gpu, model, kv_cache_size_per_token)
        prefill_time_per_token = self.calc_prefill_time_per_token(model, gpu)
        tpot = self.calc_tpot(model, gpu)

        if isinstance(prefill_time_per_token, str) or isinstance(tpot, str):
            return PerformanceMetrics(
                kv_cache_tokens=int(kv_cache_tokens),
                prefill_time_per_token=prefill_time_per_token,
                tpot=tpot,
                ttft="OOM",
                e2e_latency="OOM",
                throughput="OOM"
            )

        ttft = prefill_time_per_token + tpot / 1000
        e2e_latency = self.calc_e2e_latency(prefill_time_per_token, tpot, prompt_size, response_size)
        throughput = response_size / e2e_latency if e2e_latency > 0 else "OOM"

        return PerformanceMetrics(
            kv_cache_tokens=int(kv_cache_tokens),
            prefill_time_per_token=prefill_time_per_token,
            tpot=tpot,
            ttft=ttft,
            e2e_latency=e2e_latency,
            throughput=throughput
        )

    def evaluate_memory_footprint(self, models: List[ModelSpec], prompt_size: int, response_size: int, n_concurrent_request: int) -> List[MemoryFootprintRow]:
        results = []
        context_window = prompt_size + response_size
        for model in models:
            kv_size = self.calc_kv_cache_size_per_token(model)
            mem_footprint = self.calc_memory_footprint(model, n_concurrent_request, context_window)
            results.append(MemoryFootprintRow(
                model=model.name,
                input_size_tokens=prompt_size,
                output_size_tokens=response_size,
                concurrent_requests=n_concurrent_request,
                kv_cache_size_per_token_gib=kv_size,
                memory_footprint_gb=mem_footprint
            ))
        return results

    def evaluate_performance(self, models: List[ModelSpec], gpus: List[GPUSpec], prompt_size: int, response_size: int, n_concurrent_request: int) -> List[PerformanceRow]:
        results = []
        context_window = prompt_size + response_size
        
        for model in models:
            for gpu in gpus:
                # OOM Check similar logic to original script
                mem_footprint = self.calc_memory_footprint(model, n_concurrent_request, context_window)
                available_memory = self.num_gpu * gpu.memory_gb
                gpu_count = round(mem_footprint / available_memory, 2)
                
                # if mem_footprint > available_memory:
                #     # We do not strictly fail, we just calculate metrics, which may yield 'OOM' internally
                #     # Alternatively, we could raise OOMError here depending on strictness
                #     pass

                metrics = self.calculate_metrics(model, gpu, prompt_size, response_size)
                
                results.append(PerformanceRow(
                    model=model.name,
                    gpu=gpu.name,
                    gpu_count=gpu_count,
                    input_size_tokens=prompt_size,
                    output_size_tokens=response_size,
                    concurrent_requests=n_concurrent_request,
                    performance=metrics
                ))
        return results
