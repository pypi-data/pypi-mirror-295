# cjh-project-builder

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 개요

**cjh-project-builder**은 FastAPI 애플리케이션에서 프로젝트 구조 생성을 자동화해주는 명령어 기반 도구(CLI)입니다. 이 도구는 새로운 모듈을 생성할 때 디렉토리, 파일, 템플릿을 표준화된 형식으로 자동으로 생성하여, 시간을 절약하고 프로젝트 내에서 일관성을 유지할 수 있도록 도와줍니다.

FastAPI 백엔드 모듈을 손쉽게 추가할 수 있도록 설정된 기본 구조를 제공하며, 반복적인 작업을 간편하게 처리할 수 있습니다.

## 주요 기능

- FastAPI 프로젝트 모듈 구조를 자동으로 생성
- 디렉토리 및 파일 템플릿 지원
- 사용하기 쉬운 CLI 인터페이스 제공
- 구조 커스터마이징 가능

## 설치 방법

### Poetry로 설치

[Poetry](https://python-poetry.org/)를 통해 **cjh-project-builder**을 설치하려면, 아래 명령어를 사용하세요:

```bash
poetry add myprojectgen
```

## 사용법
설치 후, myprojectgen 명령어를 사용하여 새로운 모듈 구조를 생성할 수 있습니다.

예시
user라는 이름의 새로운 모듈 구조를 생성하려면 다음 명령어를 입력합니다:

```bash
cjh-project-builder create-structure user
```

이 명령어를 실행하면 다음과 같은 디렉토리 구조가 생성됩니다:
```css
src/
└── app/
    └── user/
        ├── __init__.py
        ├── routes.py
        ├── container.py
        ├── domain/
        │   ├── __init__.py
        │   └── user_entity.py
        ├── endpoint/
        │   ├── __init__.py
        │   └── user.py
        ├── facades/
        │   ├── __init__.py
        │   └── user_facade.py
        ├── model/
        │   ├── request/
        │   │   ├── __init__.py
        │   │   └── user_request.py
        │   └── response/
        │       ├── __init__.py
        │       └── user_response.py
        ├── repository/
        │   ├── __init__.py
        │   └── user_repository.py
        ├── services/
        │   ├── __init__.py
        │   └── user_service.py
        └── usecase/
            ├── __init__.py
            └── user_usecase.py
```

## CLI 명령어
create-structure
```bash
cjh-project-builder create-structure <module_name>
```
module_name: 생성할 모듈의 이름을 입력합니다 (예: user, order 등).

## 디렉토리 구조 설명
MyProjectGen을 사용하여 생성된 모듈 구조는 FastAPI 애플리케이션을 위한 기본적인 구성입니다. 각 모듈에는 도메인 로직, 서비스, 레포지토리, 엔드포인트 등이 포함됩니다.
```bash
src/app/<module_name>/
├── __init__.py
├── routes.py
├── container.py
├── domain/
├── endpoint/
├── facades/
├── model/
│   ├── request/
│   ├── response/
├── repository/
├── services/
└── usecase/
```