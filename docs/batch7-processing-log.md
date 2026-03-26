# Batch 7 처리 로그

> 작성일: 2026-03-19
> 처리 대상: abide-in-christ, institutes-calvin, my-utmost, streams-in-desert

---

## 요약

| 도서 슬러그 | 결정 | 이유 |
|---|---|---|
| abide-in-christ | ✅ → **true-vine(abide-in-christ)** 로 대체 처리 | Abide in Christ 텍스트 소스 없음 → 동일 저자/주제의 True Vine으로 교체 |
| institutes-calvin | ✅ 처리 완료 | Gutenberg 2권, 122 파일 |
| my-utmost | ❌ 스킵 | 저작권 문제 (1963년 갱신) |
| streams-in-desert | ❌ 스킵 | 접근 가능한 텍스트 소스 없음 |

---

## 소스 조사 결과

### 1. Abide in Christ (Andrew Murray)

- **Gutenberg**: 없음 (gutendex API로 확인)
- **CCEL**: Murray 11개 작품 목록에 없음
- **Internet Archive**: djvu 스캔본만 존재 (텍스트 추출 불가)
- **결론**: 접근 가능한 텍스트 소스 없음

**대체 결정**: 같은 저자(Andrew Murray)의 **The True Vine** (참된 포도나무) 사용
- 같은 주제 (요한복음 15장, 그리스도 안에 거함)
- 동일한 형식 (31일 묵상집)
- CCEL에 깨끗한 텍스트 제공: `https://ccel.org/ccel/m/murray/true_vine/cache/true_vine.txt`
- 슬러그: `abide-in-christ` (카탈로그 호환성 유지)

### 2. Institutes of the Christian Religion (John Calvin)

- **Gutenberg Vol.1**: `https://www.gutenberg.org/cache/epub/45001/pg45001.txt` (Book I–III 일부)
- **Gutenberg Vol.2**: `https://www.gutenberg.org/cache/epub/64392/pg64392.txt` (Book III 나머지 + Book IV)
- Book III가 두 권에 걸쳐 있음 (Vol.1: ch.I~XIII, Vol.2: ch.XIV~)

### 3. My Utmost for His Highest (Oswald Chambers)

- **저작권 문제**: Chambers 1917년 사망이지만, 미국에서 **1963년에 저작권 갱신**됨
- Gutenberg에 없음 (이 이유로 제외된 것으로 추정)
- **결론**: 법적으로 사용 불가. 스킵.

### 4. Streams in the Desert (L.B. Cowman)

- **출판**: 1925년 (미국 퍼블릭 도메인 해당)
- **Gutenberg**: 없음
- **CCEL**: 없음
- **Internet Archive**: djvu 스캔본만 (텍스트 추출 불가)
- **Sacred-texts.com**: Cloudflare 차단으로 접근 불가
- **결론**: 소스 없음. 스킵.

---

## 처리 결과

### abide-in-christ (True Vine by Andrew Murray)

- **슬러그**: `abide-in-christ`
- **원제**: The True Vine
- **저자**: 앤드류 머레이 (Andrew Murray)
- **챕터 수**: 26개 (ch01.txt ~ ch26.txt)
- **파일 위치**: `pipeline/sources/data/books/abide-in-christ/`
- **Batch 제출일**: 2026-03-19
- **Batch ID**: `batch_69bbd3bee9cc8190a3dbd823c3daa16b`
- **예상 비용**: ~$0.78

```bash
# 결과 다운로드 명령어
python -m pipeline.scripts.run_book download abide-in-christ batch_69bbd3bee9cc8190a3dbd823c3daa16b
```

### institutes-calvin (Institutes of the Christian Religion)

- **슬러그**: `institutes-calvin`
- **원제**: Institutes of the Christian Religion
- **저자**: 존 칼빈 (John Calvin)
- **파일 수**: 122개 (ch01.txt ~ ch122.txt)
  - 큰 챕터(8,000단어 초과)는 (상)/(하)/(중) 로 분할
  - 예: Book IV ch.XX = 33,257 words → ch105.txt (상) + ch106.txt (하) + ch107.txt (중)
- **파일 위치**: `pipeline/sources/data/books/institutes-calvin/`
- **Batch 제출일**: 2026-03-19
- **Batch ID**: `batch_69bbd3caf2a48190b52c0b74f8b40032`
- **예상 비용**: ~$3.66

```bash
# 결과 다운로드 명령어
python -m pipeline.scripts.run_book download institutes-calvin batch_69bbd3caf2a48190b52c0b74f8b40032
```

---

## 분할 스크립트

**파일**: `pipeline/scripts/split_books_batch7.py`

이 세션에서 두 도서를 처리하기 위해 하나의 스크립트로 통합 작성.
기존 split_books_batch1~6.py 패턴을 따르되, 두 가지 특수 케이스를 처리:

### True Vine 특수 처리

- "THE VINE"이라는 섹션 제목이 두 번 등장 (1장, 10장)
- dict로 처리하면 1장 파일이 10장으로 덮어써짐
- **해결**: `TRUE_VINE_SEQUENCE` (순서 있는 list) + `iter()` 로 순차 소비

```python
# dict 대신 ordered list 사용
TRUE_VINE_SEQUENCE = [
    ("THE VINE", 1, "포도나무 — 요한복음 15:1"),
    ...
    ("THE VINE", 10, "참 포도나무 — 요한복음 15:5"),  # 두 번째 등장
    ...
]
```

### Calvin Institutes 특수 처리

1. **두 Gutenberg 권으로 분리**: `parse_chapters_from_text()` 로 각 권 독립 파싱 후 결합
2. **Book 경계 정규식**: `r"^\s*BOOK (I{1,3}|IV)\b"` — Vol.2의 들여쓰기된 BOOK 헤더 처리
3. **Chapter 경계 정규식**: `r"^\s+CHAPTER ([IVXLC]+)\."` + `re.IGNORECASE` — Vol.1 Title Case 처리
4. **대형 챕터 분할**: 8,000단어 초과 시 단락 경계에서 분할, `(상)/(하)/(중)` 표시

---

## 주요 오류 및 해결

| 오류 | 원인 | 해결 |
|---|---|---|
| raw.txt가 CCEL 404 HTML | 다운로드 URL 잘못됨 | Gutenberg/CCEL cache URL로 교체 |
| True Vine ch01이 ch10 내용으로 덮어써짐 | "THE VINE" 중복 제목 | dict → ordered list 변환 |
| Calvin Vol.1 chapter 정규식 0개 매치 | 패턴이 ALLCAPS, 실제는 Title Case | `re.IGNORECASE` 추가 |
| Calvin BOOK 경계 정규식 0개 매치 | Vol.2 BOOK 헤더 들여쓰기 | `re.MULTILINE` + `^\s*BOOK` 패턴으로 변경 |
| Calvin 챕터가 너무 큼 (최대 33,257 단어) | Book 단위 분할 시도 | Chapter 단위 + 8,000단어 limit 분할 |
