# LLM_Sizing_Guide
A calculator to estimate the memory footprint, capacity, and latency based on your planned LLM application's requirements on different GPU architectures..

# Usage
Prerequisite: `pip install -r requirements.txt`

Here are the Flags and their abbreviations for the script.
- num_gpu ('-g'): Specify the number of GPUs you plan to use for your deployment.
- prompt_sz ('-p'): Define the average size of the input prompts you expect to process.
- response_sz ('-r'): Set the average size of the responses you expect to generate.
- n_concurrent_req ('-c'): Indicate the number of concurrent requests you anticipate handling.

By modifying these variables, you can easily estimate the performance characteristics of your LLM deployment and make informed decisions about your infrastructure requirements.

# Sample output
```bash
✗ python LLM_size_pef_calculator.py -g 4 -p 4096 -r 256 -c 10
 num_gpu = 4, prompt_size = 4096 tokens, response_size = 256 tokens
 n_concurrent_request = 10

******************** Estimate LLM Memory Footprint ********************
| Model           |   Input Size (tokens) |   Output Size (tokens) |   Concurrent Requests | KV Cache Size per Token   | Memory Footprint   |
|-----------------+-----------------------+------------------------+-----------------------+---------------------------+--------------------|
| Llama-3-8B      |                  4096 |                    256 |                    10 | 0.000122 GiB/token        | 21.31 GB           |
| Llama-3-70B     |                  4096 |                    256 |                    10 | 0.000305 GiB/token        | 153.28 GB          |
| Llama-3.1-8B    |                  4096 |                    256 |                    10 | 0.000122 GiB/token        | 21.31 GB           |
| Llama-3.1-70B   |                  4096 |                    256 |                    10 | 0.000305 GiB/token        | 153.28 GB          |
| Mistral-7B-v0.3 |                  4096 |                    256 |                    10 | 0.000122 GiB/token        | 19.31 GB           |
| Qwen2.5-14B     |                  4096 |                    256 |                    10 | 0.000183 GiB/token        | 37.37 GB           |

******************** Estimate LLM Capacity and Latency ******************** 
| Model           | GPU       |   Input Size (tokens) |   Output Size (tokens) |   Concurrent Requests |   Max # KV Cache Tokens | Prefill Time   | TPOT (ms)   | TTFT    | E2E Latency   | Output Tokens Throughput   |
|-----------------+-----------+-----------------------+------------------------+-----------------------+-------------------------+----------------+-------------+---------+---------------+----------------------------|
| Llama-3-8B      | H100 PCIe |                  4096 |                    256 |                    10 |                 1660245 | 0.005 ms       | 2.000 ms    | 0.007 s | 0.5 s         | 479.71 tokens/sec          |
| Llama-3-70B     | H100 PCIe |                  4096 |                    256 |                    10 |                  983040 | 0.046 ms       | 17.500 ms   | 0.064 s | 4.7 s         | 54.82 tokens/sec           |
| Llama-3.1-8B    | H100 PCIe |                  4096 |                    256 |                    10 |                 1660245 | 0.005 ms       | 2.000 ms    | 0.007 s | 0.5 s         | 479.71 tokens/sec          |
| Llama-3.1-70B   | H100 PCIe |                  4096 |                    256 |                    10 |                  983040 | 0.046 ms       | 17.500 ms   | 0.064 s | 4.7 s         | 54.82 tokens/sec           |
| Mistral-7B-v0.3 | H100 PCIe |                  4096 |                    256 |                    10 |                 1671168 | 0.005 ms       | 1.750 ms    | 0.006 s | 0.5 s         | 548.24 tokens/sec          |
| Qwen2.5-14B     | H100 PCIe |                  4096 |                    256 |                    10 |                 1587063 | 0.010 ms       | 3.675 ms    | 0.013 s | 1.0 s         | 261.07 tokens/sec          |
