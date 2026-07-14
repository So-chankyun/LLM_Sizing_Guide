# FastAPI 리팩토링 태스크

## Phase 3: FastAPI 스켈레톤 생성
- [x] uv 프로젝트 초기화 + 의존성 설치
- [x] `app/__init__.py` 생성
- [x] `app/main.py` — FastAPI 앱 인스턴스
- [x] `app/core/__init__.py`
- [x] `app/core/config.py` — Settings
- [x] `app/core/logging.py` — 로깅 설정
- [x] `app/core/exceptions.py` — 예외 + handler

## Phase 4: 도메인 마이그레이션
- [x] `app/domains/__init__.py`
- [x] `app/domains/calculator/__init__.py`
- [x] `app/domains/calculator/models.py` — Pydantic 모델
- [x] `app/domains/calculator/schemas.py` — 요청/응답 스키마
- [x] `app/domains/calculator/exceptions.py` — 도메인 예외
- [x] `app/domains/calculator/service.py` — 서비스 레이어
- [x] `app/api/__init__.py`
- [x] `app/api/deps.py` — 의존성 주입
- [x] `app/api/routers/__init__.py`
- [x] `app/api/routers/calculator.py` — 계산 엔드포인트
- [x] `app/api/routers/specs.py` — 스펙 조회 엔드포인트

## Phase 5: 테스트
- [x] `tests/conftest.py`
- [x] `tests/test_calculator_service.py`
- [x] `tests/test_calculator_api.py`
- [x] pytest 실행 및 통과 확인

## Phase 6: 정리
- [x] Dockerfile 생성
- [x] README.md 업데이트
- [x] 서버 기동 테스트
