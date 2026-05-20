#!/usr/bin/env python3
"""
LLM Performance Calculator

This script calculates various performance metrics for LLM inference,
including memory footprint, latency, and throughput for different
GPU and model configurations.
"""

import argparse
from typing import List, Dict, Any

from configs.gpu_specs import GPU_SPECS, GPUSpec
from configs.model_specs import MODEL_SPECS, ModelSpec
from llm_calculator.performance import PerformanceCalculator
from llm_calculator.reporting import PerformanceReporter

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Calculate LLM inference performance metrics'
    )
    parser.add_argument(
        '-g', '--num_gpu',
        type=int, default=1,
        help='Number of GPUs'
    )
    parser.add_argument(
        '-p', '--prompt_sz',
        type=int, default=4096,
        help='Prompt size in tokens'
    )
    parser.add_argument(
        '-r', '--response_sz',
        type=int, default=256,
        help='Response size in tokens'
    )
    parser.add_argument(
        '-c', '--n_concurrent_req',
        type=int, default=10,
        help='Number of concurrent requests'
    )
    return parser.parse_args()

def check_memory_requirements(
    calculator: PerformanceCalculator,
    model: ModelSpec,
    gpu: GPUSpec,
    prompt_size: int,
    response_size: int,
    n_concurrent_request: int
) -> None:
    """Check if memory requirements can be met and print warnings if not."""
    context_window = prompt_size + response_size
    # kv cache + model weights
    memory_footprint = calculator.calc_memory_footprint(
        model, n_concurrent_request, context_window
    )
    available_memory = calculator.num_gpu * gpu.memory_gb

    # 하나의 gpu 에서 해당 요청들을 감당할 수 있는지 확인
    if memory_footprint > available_memory:
        print(f"\n!!!! Warning {model.name}: n_concurrent_request={n_concurrent_request} "
              f"is TOO Large!!!\nCausing OOM with ISL={prompt_size} and OSL={response_size} "
              f"using {calculator.num_gpu}x {gpu.name}")
        
        kv_cache_size_per_token = calculator.calc_kv_cache_size_per_token(model)
        kv_cache_tokens = calculator.calc_kv_cache_tokens(
            gpu, model, kv_cache_size_per_token
        )
        # kv cache tokens(가용한 kv cache 토큰 수) / prompt size(요청당 토큰 수(input+output))
        max_n_concurrent_req = int(kv_cache_tokens // context_window)
        
        # gpu 당 최대 몇 개의 request 를 처리할 수 있는지 display
        print(f"Max number of concurrent requests that can be set for this use case: "
              f"{max_n_concurrent_req}\nIgnore the rows in the following table which "
              f"contains {gpu.name} and rerun the calculator with this number")

def calculate_memory_footprint(
    calculator: PerformanceCalculator,
    models: List[ModelSpec],
    prompt_size: int,
    response_size: int,
    n_concurrent_request: int
) -> List[Dict[str, Any]]:
    """Calculate memory footprint for all models."""
    memory_footprint_table = []
    context_window = prompt_size + response_size
    
    for model in models:
        kv_cache_size_per_token = calculator.calc_kv_cache_size_per_token(model)
        memory_footprint = calculator.calc_memory_footprint(
            model, n_concurrent_request, context_window
        )
        
        row = PerformanceReporter.format_memory_footprint_row(
            model.name,
            prompt_size,
            response_size,
            n_concurrent_request,
            kv_cache_size_per_token,
            memory_footprint
        )
        memory_footprint_table.append(row)
    
    return memory_footprint_table

def calculate_performance_metrics(
    calculator: PerformanceCalculator,
    models: List[ModelSpec],
    gpus: List[GPUSpec],
    prompt_size: int,
    response_size: int,
    n_concurrent_request: int
) -> List[Dict[str, Any]]:
    """Calculate performance metrics for all model and GPU combinations."""
    performance_table = []
    
    for model in models:
        for gpu in gpus:
            metrics = calculator.calculate_metrics(
                model, gpu, prompt_size, response_size
            )

            # model size / gpu memory
            context_window = prompt_size + response_size
            memory_footprint = calculator.calc_memory_footprint(
                                    model, n_concurrent_request, context_window
                                )
            available_memory = gpu.memory_gb

            # 소숫점으로도 나올 수 있음
            gpu_count = round(memory_footprint/available_memory, 2)
            
            row = PerformanceReporter.format_performance_row(
                model.name,
                gpu.name,
                gpu_count,
                prompt_size,
                response_size,
                n_concurrent_request,
                metrics
            )
            performance_table.append(row)
    
    return performance_table

def main() -> None:
    """Main execution function."""
    args = parse_args()
    
    print(f" num_gpu = {args.num_gpu}, prompt_size = {args.prompt_sz} tokens, "
          f"response_size = {args.response_sz} tokens")
    print(f" n_concurrent_request = {args.n_concurrent_req}")

    calculator = PerformanceCalculator(args.num_gpu)
    reporter = PerformanceReporter()

    # Calculate and report memory footprint
    memory_footprint_table = calculate_memory_footprint(
        calculator,
        MODEL_SPECS,
        args.prompt_sz,
        args.response_sz,
        args.n_concurrent_req
    )
    reporter.print_table(
        memory_footprint_table,
        "******************** Estimate LLM Memory Footprint ********************"
    )
    # memory_csv_file = reporter.save_to_csv(memory_footprint_table, 'llm_memory_footprint')

    # Check memory requirements
    for model in MODEL_SPECS:
        for gpu in GPU_SPECS:
            check_memory_requirements(
                calculator,
                model,
                gpu,
                args.prompt_sz,
                args.response_sz,
                args.n_concurrent_req
            )

    # Calculate and report performance metrics
    performance_table = calculate_performance_metrics(
        calculator,
        MODEL_SPECS,
        GPU_SPECS,
        args.prompt_sz,
        args.response_sz,
        args.n_concurrent_req
    )
    reporter.print_table(
        performance_table,
        "******************** Estimate LLM Capacity and Latency ********************"
    )
    # perf_csv_file = reporter.save_to_csv(performance_table, 'llm_performance')

    # print(f"\nResults saved to CSV files:\n1. {memory_csv_file}\n2. {perf_csv_file}")

if __name__ == '__main__':
    main()