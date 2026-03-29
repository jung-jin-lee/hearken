# 들음 (Hearken)

**시각장애인을 위한 신앙 콘텐츠 플랫폼**

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://jung-jin-lee.github.io/hearken/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 성경 1,189장 해설 · 신앙 고전 769권 · 365일 묵상을 음성으로 — 완전 무료, 앱 설치 없음

**[→ 바로 사용하기](https://jung-jin-lee.github.io/hearken/)**

---

## 소개

**들음(Hearken)**은 시각장애인과 읽기에 어려움을 느끼는 신앙인을 위해 설계된 웹 기반 신앙 콘텐츠 플랫폼입니다.

- 브라우저 내장 음성(Web Speech API)으로 모든 콘텐츠를 들을 수 있습니다
- 앱 설치 없이 스마트폰·태블릿·PC 브라우저에서 바로 접근 가능합니다
- OpenAI Batch API로 사전 생성된 콘텐츠를 정적 파일로 제공하므로 서버 비용이 없습니다

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| **성경 해설** | 구약·신약 66권 1,189장 전체 장별 해설, 묵상 질문, 기도 가이드 |
| **신앙 고전 도서관** | 청교도·개혁파·선교·한국 신앙 고전 769권 이상 |
| **매일묵상** | 365일 날짜별 큐티 콘텐츠 |
| **TTS 음성 읽기** | 재생·일시정지·속도 조절(0.5×~2.0×)·구간 이동 |
| **다크 모드** | 시스템 설정 자동 감지 |
| **진행 저장** | 마지막 위치를 자동 저장하여 이어 듣기 |

---

## 콘텐츠 현황

| 항목 | 규모 |
|------|------|
| 성경 장별 해설 | 1,189개 |
| 신앙 고전 | 769권+ (JSON 파일 34,704개) |
| 매일묵상 | 365일 |
| 전체 콘텐츠 용량 | 약 752 MB |

---

## 기술 스택

**프론트엔드**

- 순수 HTML5 / CSS3 / Vanilla JavaScript (의존성 없음)
- Web Speech API — 브라우저 내장 TTS
- WCAG 2.1 AA 접근성 준수

**콘텐츠 파이프라인** (오프라인 사전 생성)

- Python 3.x + OpenAI Batch API (GPT 모델)
- Pydantic 2.0 — 생성 결과 스키마 검증
- 생성된 JSON을 정적 파일로 저장 → 런타임 AI 호출 없음

**배포**

- GitHub Pages (정적 호스팅, 무료)
- GitHub Actions — `main` 브랜치 푸시 시 자동 배포

---

## 로컬 실행

```bash
git clone https://github.com/jung-jin-lee/hearken.git
cd hearken

# 개발 서버 시작 (기본 포트 8000)
./start-server.sh

# 커스텀 포트 사용
./start-server.sh 3000
```

브라우저에서 `http://localhost:8000` 접속

> `web/` 폴더의 HTML 파일과 `content/` 폴더의 JSON 데이터를 함께 서빙합니다.

---

## 프로젝트 구조

```
hearken/
├── web/                  # 정적 웹사이트
│   ├── index.html        # 홈페이지
│   ├── bible.html        # 성경 목록
│   ├── bible-read.html   # 성경 읽기
│   ├── devotional.html   # 매일묵상
│   ├── books.html        # 도서 목록
│   ├── book.html         # 도서 읽기
│   ├── css/              # 스타일 (접근성 포함)
│   └── js/               # TTS 컨트롤러
├── content/              # 생성된 콘텐츠 JSON
│   ├── bible/commentary/ # 성경 장별 해설
│   ├── devotional/       # 매일묵상
│   └── books/            # 신앙 고전
├── pipeline/             # 콘텐츠 생성 파이프라인
│   ├── prompts/          # GPT 프롬프트 템플릿
│   ├── batch/            # OpenAI Batch API 처리
│   ├── processors/       # 후처리 및 인덱싱
│   ├── validators/       # 스키마 검증
│   └── scripts/          # 실행 스크립트
├── docs/                 # 프로젝트 문서
└── .github/workflows/    # CI/CD (GitHub Pages 배포)
```

---

## 접근성

- **스크린리더 호환**: 시맨틱 HTML, ARIA 랜드마크 적용
- **키보드 전용 탐색**: 모든 기능을 키보드로 사용 가능
- **고대비 색상**: 명도 대비 4.5:1 이상
- **글자 크기**: rem 단위 — 브라우저 설정 글자 크기 반영
- **건너뛰기 링크**: 반복 메뉴를 건너뛰어 본문으로 바로 이동

---

## 라이선스

- **코드**: MIT License
- **콘텐츠**: 개역한글 성경 및 퍼블릭 도메인 도서를 기반으로 AI가 생성한 해설

---

## 기여

Issues와 Pull Request를 환영합니다.
버그 신고, 콘텐츠 오류 제보, 접근성 개선 제안 모두 환영합니다.

[이슈 등록하기](https://github.com/jung-jin-lee/hearken/issues)
