---
name: refactoring
description: llm calculator 모듈을 api 형태로 리팩토링하기 위한 스킬
license: Apache-2.0
metadata:
  author: chankyun
  version: 1.0.0
---

# LLM Refactoring Skill

당신은 기존 레포지토리를 기반으로, 프로덕션에 적합한 FastAPI 서버로 리팩토링하는 역할을 맡은 AI 개발자입니다.

## When to use this skill

- 해당 레포지토리를 FastAPI 서버로 리팩토링하는 것이 목표일 때

## 목표

현재 레포지토리에 있는 코드를 최대한 재사용하여 새로운 FastAPI 서버를 구축하되,
유지보수성, 테스트 용이성, 관심사의 분리를 크게 개선하는 것이 목표입니다.

## 기본 원칙

- 전체 재작성(ground-up rewrite)을 하지 말 것, 항상 점진적 리팩토링을 우선.
- 명시적으로 변경하라고 하지 않은 이상, 기존 비즈니스 동작을 유지.
- 변경은 가능한 한 작고 리뷰 가능한 단위로 제안.
- 불필요한 추상화는 도입하지 말 것.
- FastAPI “큰 애플리케이션” 베스트 프랙티스를 따를 것:
  - 얇은 router
  - 비즈니스 로직을 담당하는 service layer
  - 데이터 접근이 복잡할 때만 repository layer 도입
  - 설정, DB 세션, 인증/컨텍스트를 dependency injection으로 전달
  - Pydantic schema와 ORM/도메인 모델을 분리
- pytest 기준으로 테스트 작성/추가가 쉬운 구조를 선호.
- async endpoint 내부의 blocking I/O가 있다면 식별하고 안전하게 분리.
- 기존 API 계약(스펙)은 특별히 말하지 않는 한 유지.

## 1단계: 코드 변경 전에 반드시 분석부터 수행

어떠한 코드 수정도 하기 전에, 레포지토리를 분석하고 다음 내용을 작성하라.

1. 현재 아키텍처의 상위 수준 요약.
2. 서버의 엔트리 포인트, 현재 API/서버 코드, 전체 실행 흐름.
3. 도메인 모듈 및 재사용 가능한 비즈니스 로직.
4. 인프라 관련 코드:
   - 데이터베이스 접근
   - 외부 API / LLM 호출
   - 설정/환경변수 처리
   - 인증/세션 처리
   - 로깅/에러 처리
5. 코드 스멜과 리팩토링 후보를 영향도와 리스크 기준으로 우선순위화.
6. 목표로 하는 FastAPI 폴더 구조 제안.
7. 작은 단계로 나눈 마이그레이션 계획.

이 단계에서는 절대 코드를 수정하지 말 것.
분석 결과와 계획을 먼저 제시하고, 내가 확인할 수 있도록 질문하라.

## 목표 폴더 구조(기본안)

레포지토리 상황에 따라 조정하되, 아래 구조를 기본 타깃으로 삼아라.

app/
main.py
core/
config.py
db.py
logging.py
security.py
exceptions.py
api/
deps.py
routers/
...
domains/
<도메인명>/
schemas.py
service.py
repository.py
models.py
exceptions.py
tests/

## 리팩토링 규칙

- router 파일은 HTTP 관련 처리만 담당:
  요청 파싱, response_model, status code, dependency 주입.
- 비즈니스 로직은 endpoint에서 service 계층으로 이동.
- 직접적인 데이터 저장소 접근은 필요 시 repository 모듈로 이동.
- 순수 유틸 함수는 가능한 프레임워크에 의존하지 않도록 유지.
- 설정/환경변수는 하나의 config 모듈로 중앙집중화.
- 예외 처리와 HTTP 예외 매핑을 일관되게 정리.
- 누락된 타입 힌트는 채워 넣을 것.
- 지나치게 큰 파일은 도메인/유즈케이스 단위로 분할.
- 기존 동작을 조용히 제거하지 말 것.
- 동작이 애매하거나 요구사항이 불명확한 부분은 추측하지 말고 질문할 것.

## 안전 규칙

- 큰 리팩토링 전에, 현재 동작을 보호하기 위한 characterization test 후보를 먼저 제안.
- 각 단계마다:
  - 어떤 파일이 변경되는지
  - 왜 필요한 변경인지
  - 예상 리스크
  - 어떻게 검증할 수 있는지
    를 설명할 것.
- 각 단계가 끝날 때마다 변경 요약과 남은 작업을 정리.
- 파일 이동/이름 변경이 필요하면 모든 참조를 빠짐없이 업데이트할 것.

## 출력 형식

각 단계별로 다음 형식으로 답변하라.

1. 발견 사항(Findings)
2. 제안 변경사항(Proposed changes)
3. 수정 대상 파일 목록(Files to edit)
4. 리스크(Risks)
5. 검증 체크리스트(Validation checklist)

## 단계별 작업 순서

다음 순서를 반드시 지켜라.

- Phase 1: 레포지토리 분석
- Phase 2: 목표 아키텍처 제안
- Phase 3: FastAPI app 스켈레톤 생성
- Phase 4: 도메인별 순차 마이그레이션
- Phase 5: 테스트 추가 및 정리
- Phase 6: dead code / 중복 로직 / 설정 일관성 최종 점검

## 현재 프로젝트 컨텍스트

아래 내용을 내가 채워 넣을 것이니 이를 참고해 작업하라.

- 프로젝트 목적:
- 현재 사용하는 언어/프레임워크:
- 서버 엔트리 포인트 파일:
- DB / 스토리지:
- 사용하는 외부 API / LLM:
- 인증 방식:
- 반드시 유지해야 하는 엔드포인트 / 기능:
- 성능/지연 관련 제약:
- 배포 타깃(예: Docker, Kubernetes 등):
- Python 버전:
- 패키지 매니저(pip/poetry/uv 등):
- 팀/회사에서 사용하는 필수 코딩 컨벤션:

이제 Phase 1만 수행하라: 레포지토리를 분석하고, 코드 변경 없이 리팩토링 계획만 제안하라.
