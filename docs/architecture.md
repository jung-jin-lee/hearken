# Hearken (들음): 시각장애인을 위한 신앙 콘텐츠 플랫폼 구현 계획

## Context

시각장애인은 세계 최대 미전도 집단(복음 접촉률 5~15%)이며, 점자 성경은 전체 번역 언어의 10% 미만에서만 제공된다. 이 프로젝트는 OpenAI GPT-5.4 API 크레딧 $8,000(만료 ~2주)을 활용해 양질의 신앙 콘텐츠를 사전 생성하고, 접근성 최적화 정적 웹사이트 + Web Speech API로 시각장애인에게 제공한다.

**핵심 결정사항:**
- AI는 콘텐츠 **사전 생성**에만 사용 (런타임 AI 없음)
- 웹: 순수 HTML/CSS/JS (프레임워크 없음)
- 파이프라인: Python + OpenAI Batch API (50% 할인)
- 음성: Web Speech API (브라우저 내장 TTS, 무료)
- 언어: 한국어 우선
- 범위: 장 단위 해설 (절 단위는 추후 확장)

---

## 1. 생성할 콘텐츠 목록

| # | 콘텐츠 | 항목 수 | 비고 |
|---|--------|--------|------|
| 1 | 성경 66권 개론 (배경, 핵심메시지, 개요) | 66 | |
| 2 | 성경 장별 해설 + 묵상질문 3개 + 기도 가이드 | 1,189 | 핵심 콘텐츠 |
| 3 | 365일 매일 묵상 (본문+해설+기도문) | 365 | |
| 4 | 성경 인물 해설 | 50 | |
| 5 | 주제별 성경 가이드 (기도, 믿음, 사랑 등) | 30 | |
| 6 | 주요 구절 500선 심층 해설 | 500 | |
| 7 | 퍼블릭 도메인 도서 현대어 번역 + 요약 | ~300장 | 고전 20~30권 |

---

## 2. 비용 추정 (Batch API: $1.25/1M input, $7.50/1M output)

| 콘텐츠 | 항목 | 입력 토큰 | 출력 토큰 | 비용 |
|--------|------|----------|----------|------|
| 성경 장별 해설 | 1,189 | 2.4M | 1.8M | $16.50 |
| 365일 묵상 | 365 | 0.4M | 0.3M | $2.75 |
| 66권 개론 | 66 | 0.03M | 0.07M | $0.56 |
| 인물/주제/구절 | 580 | 0.8M | 1.2M | $10.00 |
| 도서 가공 | 300 | 0.9M | 0.3M | $3.38 |
| **소계** | | **4.53M** | **3.67M** | **$33.19** |
| QA 재생성 (15%) | | | | $5.00 |
| 프롬프트 반복/테스트 | | | | $100.00 |
| **총계** | | | | **~$140** |
| **잔여 예산** | | | | **~$7,860** |

> 잔여 예산은 콘텐츠 품질 개선, 추가 도서 가공, 향후 다국어 확장에 활용

---

## 3. 기술 아키텍처

```
[콘텐츠 생성 - 2주간]
Python 스크립트 → 프롬프트 빌더 → .jsonl 생성 → OpenAI Batch API
                                                    ↓ (24시간 내 처리)
                                            결과 다운로드 → QA 검증 → JSON 파일

[서비스 - 이후 지속]
정적 웹사이트 (HTML/CSS/JS)
├── 콘텐츠 JSON 로드
├── 접근성 네비게이션 (키보드, ARIA)
├── Web Speech API (브라우저 TTS)
└── 정적 호스팅 (GitHub Pages / Vercel)
```

---

## 4. 프로젝트 구조

```
blind-ai/
├── docs/                           # 기존 조사 문서
│   ├── blind-evangelization-status.md
│   ├── faith-book-catalog.md
│   └── architecture.md             # 이 설계 문서
│
├── pipeline/                       # 콘텐츠 생성 파이프라인
│   ├── requirements.txt            # openai, pydantic, httpx
│   ├── config.py                   # API 키, 모델 설정, 경로
│   │
│   ├── sources/                    # 원본 텍스트 수집
│   │   ├── bible_kr.py             # 개역한글 성경 텍스트 로더
│   │   ├── gutenberg.py            # Gutenberg 텍스트 다운로더
│   │   └── data/                   # 다운로드된 원본 텍스트
│   │
│   ├── prompts/                    # 프롬프트 템플릿
│   │   ├── base.py                 # 공통 시스템 프롬프트
│   │   ├── bible_commentary.py     # 장별 해설
│   │   ├── devotional.py           # 365일 묵상
│   │   ├── book_intro.py           # 66권 개론
│   │   ├── character.py            # 인물 해설
│   │   ├── topic.py                # 주제별 가이드
│   │   ├── key_verse.py            # 주요 구절 해설
│   │   └── book_processing.py      # 도서 현대어 번역
│   │
│   ├── batch/                      # Batch API 인터페이스
│   │   ├── builder.py              # 프롬프트 → .jsonl 변환
│   │   ├── submitter.py            # Batch 제출 + 상태 폴링
│   │   ├── downloader.py           # 결과 다운로드
│   │   └── requests/               # 생성된 .jsonl 파일
│   │
│   ├── validators/                 # QA 검증
│   │   ├── schema_validator.py     # JSON 스키마 검증
│   │   ├── completeness.py         # 누락 항목 체크
│   │   └── reference_check.py      # 성경 구절 참조 정확성
│   │
│   ├── processors/                 # 후처리
│   │   ├── structurer.py           # 원시 출력 → 최종 JSON
│   │   └── indexer.py              # 콘텐츠 매니페스트 생성
│   │
│   └── scripts/                    # 실행 스크립트
│       ├── 01_fetch_sources.py     # 원본 텍스트 수집
│       ├── 02_run_pilot.py         # 파일럿 (창세기 10장)
│       ├── 03_run_bible.py         # 성경 해설 전체
│       ├── 04_run_devotional.py    # 365일 묵상
│       ├── 05_run_supplementary.py # 인물/주제/구절
│       ├── 06_run_books.py         # 도서 가공
│       └── 07_run_qa.py            # QA 전체 실행
│
├── content/                        # 생성된 콘텐츠 (출력)
│   ├── manifest.json               # 전체 콘텐츠 인덱스
│   ├── bible/
│   │   ├── introductions/          # {book}.json
│   │   ├── commentary/             # {book}/{chapter}.json
│   │   ├── characters/             # {name}.json
│   │   ├── topics/                 # {topic}.json
│   │   └── key-verses/             # key-verses.json
│   ├── devotional/                 # {month}/{day}.json
│   └── books/                      # {book-slug}/{chapter}.json
│
├── web/                            # 정적 웹사이트
│   ├── index.html                  # 랜딩 페이지
│   ├── bible.html                  # 성경 브라우저
│   ├── devotional.html             # 매일 묵상
│   ├── books.html                  # 도서관
│   ├── search.html                 # 검색
│   ├── css/
│   │   ├── reset.css
│   │   ├── accessibility.css       # 고대비, 포커스, 크기 조절
│   │   └── main.css
│   └── js/
│       ├── content-loader.js       # JSON → DOM 렌더링
│       ├── tts-controller.js       # Web Speech API 래퍼
│       ├── navigation.js           # 키보드 내비게이션
│       ├── search.js               # 클라이언트 검색
│       └── bookmarks.js            # localStorage 북마크
│
└── tests/
    ├── test_builder.py
    ├── test_validators.py
    └── test_processors.py
```

---

## 5. JSON 스키마 (핵심)

### 장별 해설
```json
{
  "book": "genesis",
  "book_kr": "창세기",
  "chapter": 1,
  "text": "태초에 하나님이 천지를 창조하시니라...",
  "commentary": "창세기 1장은 하나님의 창조 사역을...",
  "key_themes": ["창조", "하나님의 주권"],
  "questions": ["...묵상질문1", "...2", "...3"],
  "prayer": "하나님 아버지, ...",
  "cross_references": ["시편 19:1", "요한복음 1:1-3"]
}
```

### 매일 묵상
```json
{
  "day": 1, "month": 1,
  "title": "새해의 시작, 하나님과 함께",
  "reference": "여호수아 1:9",
  "text": "내가 네게 명령한 것이 아니냐...",
  "reading": "새해를 맞이하며...",
  "question": "올해 하나님께서...",
  "prayer": "사랑하는 하나님..."
}
```

---

## 6. 웹 접근성 설계

### WCAG 2.1 AA 준수
- 시맨틱 HTML5: `<nav>`, `<main>`, `<article>`, `<section>`
- ARIA 랜드마크, 라벨, 라이브 리전
- 건너뛰기 링크 (`<a href="#main" class="skip-link">본문으로 이동</a>`)
- 고대비 (4.5:1 이상), rem 단위 글자 크기
- 키보드 전용 내비게이션 + 포커스 인디케이터
- 언어 선언 (`lang="ko"`)

### Web Speech API TTS 컨트롤
- 재생/일시정지/속도 조절 (0.5x~2.0x)
- 섹션 단위 이동 (본문 → 해설 → 질문 → 기도)
- Chrome 15초 버그 대응: 문장 단위 청킹
- 한국어 음성 선택기
- ARIA live region으로 재생 상태 안내

### 콘텐츠 내비게이션 구조
```
홈 → 성경 → 구약/신약 → 책 → 장 → (본문|해설|질문|기도)
   → 매일묵상 → 월 → 일
   → 도서관 → 책 → 장
   → 주제별 → 주제
   → 인물 → 인물명
   → 검색
```

---

## 7. 2주 실행 계획

### Week 1: 파이프라인 + 핵심 콘텐츠 생성

| 일 | 작업 |
|----|------|
| **1~2일** | 프로젝트 초기화, Python 환경 구성, 성경 텍스트 수집, 프롬프트 템플릿 작성, Batch API 빌더/서브미터 구현 |
| **3일** | 파일럿 배치 (창세기 10장) → 품질 검토 → 프롬프트 조정 |
| **4일** | 성경 장별 해설 전체 배치 제출 (1,189장) + 66권 개론 + 인물 50 + 주제 30 |
| **5일** | 배치 결과 수신 + QA 검증 + 365일 묵상 배치 제출 + 주요구절 500 제출 |
| **6일** | 퍼블릭 도메인 도서 텍스트 수집 + 도서 가공 배치 제출 |
| **7일** | 전체 QA 실행, 실패 항목 재생성, JSON 후처리 + 인덱스 생성 |

### Week 2: 웹사이트 + 마무리

| 일 | 작업 |
|----|------|
| **8~9일** | HTML 구조 + CSS 접근성 + 콘텐츠 로더 구현 |
| **10~11일** | Web Speech API TTS 컨트롤러 + 키보드 내비게이션 + 검색 |
| **12일** | 도서 가공 결과 통합 + 북마크 기능 |
| **13일** | 스크린리더 테스트 (VoiceOver) + 접근성 점검 + 버그 수정 |
| **14일** | 배포 (GitHub Pages/Vercel) + 최종 테스트 |

---

## 8. QA 전략

| 검증 유형 | 방법 | 대상 |
|----------|------|------|
| 스키마 검증 | pydantic 모델로 자동 검증 | 전체 출력 |
| 완전성 체크 | 누락 장/일/항목 자동 탐지 | 전체 |
| 구절 참조 검증 | 성경 구절 존재 여부 자동 확인 | cross_references |
| 접근성 언어 체크 | 시각 은유 표현 탐지 ("보세요" 등) | 전체 텍스트 |
| 수동 신학 검토 | 66권 개론 전수 + 해설 10% 샘플링 | 주요 콘텐츠 |

---

## 9. 핵심 기술 결정

| 결정 | 이유 |
|------|------|
| Web Speech API (OpenAI TTS 아님) | 무료, 런타임 AI 불필요, 예산 절약 |
| Batch API (실시간 아님) | 50% 할인, 3만+ 요청 처리에 적합 |
| 순수 HTML/CSS/JS | 스크린리더 호환성 최고, 빌드 불필요 |
| 개역한글판 | 퍼블릭 도메인, 저작권 문제 없음 |
| 장 단위 해설 우선 | 2주 내 완료 확실, 절 단위는 추후 확장 |
| 한국어 우선 | 핵심 타겟, 다국어는 잔여 예산으로 확장 |

---

## 10. 검증 방법

1. **파이프라인**: `python pipeline/scripts/02_run_pilot.py` → 창세기 10장 결과 확인
2. **QA**: `python pipeline/scripts/07_run_qa.py` → 전체 스키마/완전성 검증
3. **웹사이트**: 로컬에서 `python -m http.server` → 브라우저 접근성 검사
4. **스크린리더**: macOS VoiceOver로 전체 페이지 탐색 테스트
5. **TTS**: Web Speech API 재생 → 챕터 이동, 속도 조절, 한국어 음성 확인
6. **배포 후**: Lighthouse 접근성 점수 90+ 확인
