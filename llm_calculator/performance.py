"""Performance calculation utilities for LLM inference."""

from dataclasses import dataclass
from typing import Union, Optional
from configs.gpu_specs import GPUSpec
from configs.model_specs import ModelSpec

BYTES_IN_GiB = 1_073_741_824

@dataclass
class PerformanceMetrics:
    kv_cache_tokens: int
    prefill_time_per_token: Union[float, str]
    tpot: Union[float, str]
    ttft: Union[float, str]
    e2e_latency: Union[float, str]
    throughput: Union[float, str]

class PerformanceCalculator:
    """
    PerformanceCalculator 클래스를 초기화합니다.

    Args:
        num_gpu: 사용할 GPU의 개수입니다.
    Description:
        - gpu 가 2개 이상일 경우 tensor parallelism 으로 모델을 분산하여 서빙하였다고 가정
        - 분산된 모델을 통하여 요청을 처리한다고 가정
        - 모델의 가중치 양자화는 고려되지 않음.(모든 파라미터를 fp16 으로 가정)
        - gpu 종류에 따른 추론 가능 정밀도가 고려되지 않음
        - batch size 고려되지 않음
        - data parallel 고려되지 않음
    """

    def __init__(self, num_gpu: int):
        self.num_gpu = num_gpu

    def calc_kv_cache_size_per_token(self, model: ModelSpec) -> float:
        """Calculate KV cache size per token in GiB."""
        d_head = model.d_model / model.n_heads
        bytes_per_value = 2  # FP16 = 2 bytes
        return 2 * model.n_layers * model.n_kv_heads * d_head * bytes_per_value / BYTES_IN_GiB

    def calc_memory_footprint(self,
                            model: ModelSpec,
                            n_concurrent_request: int,
                            context_window: int) -> float:
        """Calculate total memory footprint in GB."""
        kv_cache_size_per_token = self.calc_kv_cache_size_per_token(model)
        return (kv_cache_size_per_token * context_window * n_concurrent_request +
                model.params_billion * 2)

    def calc_kv_cache_tokens(self,
                           gpu: GPUSpec,
                           model: ModelSpec,
                           kv_cache_size: float) -> float:
        """Calculate maximum number of tokens that can fit in KV cache."""
        result = (self.num_gpu * gpu.memory_gb - 2 * model.params_billion) / kv_cache_size
        return max(0, result)

    def calc_prefill_time_per_token(self,
                                  model: ModelSpec,
                                  gpu: GPUSpec) -> Union[float, str]:
        """Calculate prefill time per token in milliseconds."""
        result = (2 * model.params_billion / self.num_gpu) / gpu.fp16_tflops
        return result if result >= 0 else "OOM"

    def calc_tpot(self,
                 model: ModelSpec,
                 gpu: GPUSpec) -> Union[float, str]:
        """Calculate token processing time (TPOT) in milliseconds."""
        result = (2 * model.params_billion / self.num_gpu) / gpu.memory_bandwidth_gbps * 1000
        return result if result >= 0 else "OOM"

    def calc_e2e_latency(self,
                        prefill_time_per_token: float,
                        tpot: float,
                        prompt_size: int,
                        response_size: int) -> float:
        """Calculate end-to-end latency in seconds."""
        return (prompt_size * prefill_time_per_token + response_size * tpot) / 1000

    def calculate_metrics(self,
                        model: ModelSpec,
                        gpu: GPUSpec,
                        prompt_size: int,
                        response_size: int) -> PerformanceMetrics:
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
        e2e_latency = self.calc_e2e_latency(
            prefill_time_per_token, tpot, prompt_size, response_size
        )
        throughput = response_size / e2e_latency if e2e_latency > 0 else "OOM"

        return PerformanceMetrics(
            kv_cache_tokens=int(kv_cache_tokens),
            prefill_time_per_token=prefill_time_per_token,
            tpot=tpot,
            ttft=ttft,
            e2e_latency=e2e_latency,
            throughput=throughput
        )
