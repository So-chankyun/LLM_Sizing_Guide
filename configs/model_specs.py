"""Model specifications for LLM performance calculations."""

from dataclasses import dataclass
from typing import List

@dataclass
class ModelSpec:
    name: str
    params_billion: float
    d_model: int
    n_heads: int
    n_kv_heads: int
    n_layers: int
    max_context_window: int

MODEL_SPECS: List[ModelSpec] = [
    # ModelSpec(
    #     "Llama-3.1-8B", 8, 4096, 32, 8, 32, 131072
    # ),
    # ModelSpec(
    #     "Llama-3.1-70B", 70, 8192, 64, 8, 80, 131072
    # ),
    # ModelSpec(
    #     "Mistral-7B-v0.3", 7, 4096, 32, 8, 32, 32768
    # ),
    # ModelSpec(
    #     "Qwen2.5-14B", 14.7, 5120, 40, 8, 48, 131072
    # )
    ModelSpec(
        "GPT-OSS-120B",117,2880,36,8,36,131072
    )
]

# Commented out models for reference
"""
LEGACY_MODEL_SPECS = [
    ModelSpec("Llama-3-8B", 8, 4096, 32, 8, 32, 8192),
    ModelSpec("Llama-3-70B", 70, 8192, 64, 8, 80, 8192),
    ModelSpec("Llama-2-7B", 7, 4096, 32, 32, 32, 8192),  # Uses MHA
    ModelSpec("Falcon-7B", 7, 4544, 71, 1, 32, 2048),    # Uses MQA
    ModelSpec("Falcon-40B", 40, 8192, 128, 1, 60, 2048), # Uses MQA
    ModelSpec("Falcon-180B", 180, 14848, 232, 1, 80, 2048), # Uses MQA
]
"""