# LSW Quiz 프로젝트

## 프로젝트 개요

LSW Quiz는 FastAPI와 PostgreSQL을 기반으로 개발된 퀴즈 생성 및 응시 플랫폼입니다. 이 프로젝트는 사용자가 퀴즈를 생성하고, 다른 사용자들이 퀴즈에 참여하여 지식을 테스트할 수 있는 웹 애플리케이션입니다.

### 주요 기능

- **사용자 관리**: 회원가입, 로그인, 프로필 관리
- **퀴즈 생성**: 다양한 유형의 퀴즈 생성 및 관리
- **퀴즈 응시**: 생성된 퀴즈에 참여하고 점수 획득
- **결과 분석**: 퀴즈 응시 결과 및 통계 확인
- **관리자 기능**: 사용자 및 퀴즈 관리

## 기술 스택

- **백엔드**: FastAPI, SQLAlchemy, Alembic
- **데이터베이스**: PostgreSQL
- **캐싱**: Redis
- **인증**: JWT (JSON Web Tokens)
- **컨테이너화**: Docker, Docker Compose
- **패키지 관리**: Poetry

## 시스템 요구사항

- Python 3.9 이상
- Docker 및 Docker Compose
- PostgreSQL 15
- Redis 7

## 설치 및 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/saohwan/lsw_quiz.git
cd lsw_Quiz
```

### 2. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가합니다:

```
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/quiz_db

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
DEBUG=True
ENVIRONMENT=development
```

### 3. Docker Compose로 실행

```bash
docker-compose up --build
```

이 명령어는 다음 작업을 수행합니다:
- 필요한 Docker 이미지 빌드
- PostgreSQL 및 Redis 컨테이너 실행
- 데이터베이스 마이그레이션 실행
- FastAPI 애플리케이션 서버 실행

### 4. 로컬 개발 환경 설정 (Docker 없이)

Poetry를 사용하여 로컬 개발 환경을 설정할 수 있습니다:

```bash
# Poetry 설치
pip install poetry==2.1.2

# 의존성 설치
poetry install

# 가상 환경 활성화
poetry shell

# 데이터베이스 마이그레이션
alembic upgrade head

# 애플리케이션 실행
uvicorn app.main:app --reload
```

## API 문서

애플리케이션이 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 프로젝트 구조

```
lsw_quiz/
├── alembic/                  # 데이터베이스 마이그레이션
├── app/                      # 애플리케이션 코드
│   ├── api/                  # API 엔드포인트
│   │   └── endpoints/        # 각 기능별 엔드포인트
│   ├── core/                 # 핵심 설정 및 유틸리티
│   ├── models/               # SQLAlchemy 모델
│   ├── schemas/              # Pydantic 스키마
│   └── utils/                # 유틸리티 함수
├── tests/                    # 테스트 코드
├── .env                      # 환경 변수
├── alembic.ini               # Alembic 설정
├── docker-compose.yml        # Docker Compose 설정
├── Dockerfile                # Docker 이미지 설정
├── poetry.lock               # Poetry 의존성 잠금 파일
└── pyproject.toml            # Poetry 프로젝트 설정
```

## 데이터베이스 마이그레이션

데이터베이스 스키마를 변경할 때는 Alembic을 사용하여 마이그레이션을 생성하고 적용합니다:

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "마이그레이션 설명"

# 마이그레이션 적용
alembic upgrade head
```
