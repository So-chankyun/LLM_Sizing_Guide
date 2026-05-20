## 1. 개요
  - LLM 모델을 특정 GPU에서 구동시킬 때 필요한 메모리, latency, throughput 등을 계산하는 코드입니다.
  - 주요 파라미터는 다음과 같습니다.
    - `num_gpu` ('-g'): 배포에 사용할 GPU 개수를 지정합니다.
    - `prompt_sz` ('-p'): 처리할 입력 프롬프트의 평균 크기(토큰 수)를 정의합니다.
    - `response_sz` ('-r'): 생성할 응답의 평균 크기(토큰 수)를 설정합니다.
    - `n_concurrent_req` ('-c'): 예상되는 동시 요청(Concurrent Requests) 수를 입력합니다.

## 2 가상환경 셋팅
### 2.1 가상환경 생성
```bash
# python 3.10 이상
python -m venv .venv

# 윈도우
.venv\Scripts\activate
```
  
### 2.2 필요한 라이브러리 설치
  - 다음 명령을 수행하여 필요한 라이브러리를 설치합니다.
```bash
pip install --no-index --find-links=./wheels/ -r requirements.txt
```

## 3. 코드 실행
```bash
python LLM_size_pef_calculator.py -g 1 -p 4096 -r 256 -c 10
```

## 4. 결과 확인
### 4.1 주요 항목
- `KV Cache Size per Token`: KV 캐시가 토큰 하나당 차지하는 메모리양입니다. (FP16 기준: 2 bytes/token)
- `Memory Footprint`: 모델 가중치, 옵티마이저 상태, KV 캐시 등을 모두 합한 총 메모리 사용량입니다.
- `Max # KV Cache Tokens`: 주어진 GPU 메모리 내에서 처리 가능한 최대 토큰 수입니다.
- `Prefill Time`: 입력 프롬프트를 처리하는 데 걸리는 시간입니다.
- `TPOT (Time Per Output Token)`: 응답 토큰 하나를 생성하는 데 걸리는 시간입니다.
- `TTFT (Time To First Token)`: 첫 번째 응답 토큰이 생성되기까지 걸리는 시간입니다.
- `E2E Latency`: 전체 요청이 완료되기까지 걸리는 총 시간입니다.
- `Output Tokens Throughput`: 초당 생성 가능한 출력 토큰 수입니다.

```bash
# Example 
(.venv) C:\code\LLM_Sizing_Guide>python LLM_size_pef_calculator.py -g 4 -p 4096 -r 256 -c 10
 num_gpu = 4, prompt_size = 4096 tokens, response_size = 256 tokens
 n_concurrent_request = 10

******************** Estimate LLM Memory Footprint ********************
| Model        |   Input Size (tokens) |   Output Size (tokens) |   Concurrent Requests | KV Cache Size per Token   | Memory Footprint   |
|--------------+-----------------------+------------------------+-----------------------+---------------------------+--------------------|
| GPT-OSS-120B |                  4096 |                    256 |                    10 | 0.000086 GiB/token        | 237.74 GB          |

******************** Estimate LLM Capacity and Latency ********************
| Model        | GPU Type       |   Mininum GPU Count |   Input Size (tokens) |   Output Size (tokens) |   Concurrent Requests |   Max # KV Cache Tokens | Prefill Time   | TPOT (ms)   | TTFT    | E2E Latency   | Output Tokens Throughput   |
|--------------+----------------+---------------------+-----------------------+------------------------+-----------------------+-------------------------+----------------+-------------+---------+---------------+----------------------------|
| GPT-OSS-120B | A100 80GB PCIe |                2.97 |                  4096 |                    256 |                    10 |                 1001972 | 0.188 ms       | 30.233 ms   | 0.218 s | 8.5 s         | 30.09 tokens/sec           |
| GPT-OSS-120B | H100 80GB PCIe |                2.97 |                  4096 |                    256 |                    10 |                 1001972 | 0.077 ms       | 29.250 ms   | 0.107 s | 7.8 s         | 32.80 tokens/sec           |
| GPT-OSS-120B | H200 141GB SXM |                1.69 |                  4096 |                    256 |                    10 |                 3844778 | 0.059 ms       | 12.188 ms   | 0.071 s | 3.4 s         | 76.14 tokens/sec           |
| GPT-OSS-120B | H200 141GB NVL |                1.69 |                  4096 |                    256 |                    10 |                 3844778 | 0.070 ms       | 12.188 ms   | 0.082 s | 3.4 s         | 75.14 tokens/sec           |
| GPT-OSS-120B | B300 288GB SXM |                0.83 |                  4096 |                    256 |                    10 |                10695475 | 0.026 ms       | 7.312 ms    | 0.033 s | 2.0 s         | 129.39 tokens/sec          |

```
- 만약 주어진 요청량을 처리할 수 없다면, 다음과 같은 알림이 발생하게 됩니다.
```bash
(.venv) C:\code\LLM_Sizing_Guide>python LLM_size_pef_calculator.py -g 1 -p 4096 -r 256 -c 10
 num_gpu = 1, prompt_size = 4096 tokens, response_size = 256 tokens
 n_concurrent_request = 10

******************** Estimate LLM Memory Footprint ********************
| Model        |   Input Size (tokens) |   Output Size (tokens) |   Concurrent Requests | KV Cache Size per Token   | Memory Footprint   |
|--------------+-----------------------+------------------------+-----------------------+---------------------------+--------------------|
| GPT-OSS-120B |                  4096 |                    256 |                    10 | 0.000086 GiB/token        | 237.74 GB          |

!!!! Warning GPT-OSS-120B: n_concurrent_request=10 is TOO Large!!!
Causing OOM with ISL=4096 and OSL=256 using 1x A100 80GB PCIe
Max number of concurrent requests that can be set for this use case: 0
Ignore the rows in the following table which contains A100 80GB PCIe and rerun the calculator with this number

!!!! Warning GPT-OSS-120B: n_concurrent_request=10 is TOO Large!!!
Causing OOM with ISL=4096 and OSL=256 using 1x H100 80GB PCIe
Max number of concurrent requests that can be set for this use case: 0
Ignore the rows in the following table which contains H100 80GB PCIe and rerun the calculator with this number

!!!! Warning GPT-OSS-120B: n_concurrent_request=10 is TOO Large!!!
Causing OOM with ISL=4096 and OSL=256 using 1x H200 141GB SXM
Max number of concurrent requests that can be set for this use case: 0
Ignore the rows in the following table which contains H200 141GB SXM and rerun the calculator with this number

!!!! Warning GPT-OSS-120B: n_concurrent_request=10 is TOO Large!!!
Causing OOM with ISL=4096 and OSL=256 using 1x H200 141GB NVL
Max number of concurrent requests that can be set for this use case: 0
Ignore the rows in the following table which contains H200 141GB NVL and rerun the calculator with this number
```
### 4.2 결과 해석
위의 예시 실행 결과(`GPT-OSS-120B` 모델 기준)를 통해 다음과 같은 정보를 확인할 수 있습니다.

- **모델 배치 및 메모리 요구량**:
  - `GPT-OSS-120B` 모델을 구동하기 위해서는 약 **237.74 GB**의 총 메모리(`Memory Footprint`)가 필요합니다.
  - 이에 따라 `Minimum GPU Count`를 보면, **A100 80GB** 모델은 최소 **3대**(2.97대), **H200 141GB** 모델은 최소 **2대**(1.69대)가 필요함을 알 수 있습니다.

- **성능 분석 (Latency & Throughput)**:
  - **응답 속도**: 최신 GPU일수록 성능이 비약적으로 향상됩니다. 예를 들어, **B300 288GB**는 **E2E Latency**가 **2.0초**로, **A100(8.5초)** 대비 약 4배 이상 빠릅니다.
  - **첫 토큰 생성 시간(TTFT)**: 사용자 경험에 직접적인 영향을 주는 **TTFT** 역시 B300이 **0.033초**로 매우 짧습니다.
  - **처리량(Throughput)**: 초당 생성되는 토큰 수(`Output Tokens Throughput`)를 비교하여 시스템이 초당 어느 정도의 부하를 견딜 수 있는지 판단할 수 있습니다.

- **최대 수용 용량**:
  - `Max # KV Cache Tokens`는 해당 GPU 구성에서 메모리 내에 보관할 수 있는 최대 토큰 수를 나타내며, 동시 접속자 수 증가 시 참고할 수 있는 지표입니다.


## 5. 참고 사항
- gpu 가 2개 이상일 경우 TP(tensor parallel)로 모델을 분산하여 서빙하였다고 가정
- 분산된 모델을 통하여 요청을 처리한다고 가정
- 모델의 가중치 양자화는 고려되지 않음.(모든 파라미터를 fp16 으로 가정)
- GPU 종류에 따른 추론 가능 정밀도가 고려되지 않음
- Inference Batch Size 고려되지 않음
- DP(data parallel) 고려되지 않음 



