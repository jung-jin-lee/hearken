# Batch 14-15 처리 로그

> 제출일: 2026-03-23
> 완료일: 2026-03-23
> 상태: ✅ 완료 (19/19권, 311/311챕터, 실패 0)

## Batch 14 — Gutenberg 소스 9권

| slug | 챕터 | 비용 | Batch ID |
|------|------|------|----------|
| moody-way-to-god | 9 | $0.27 | batch_69c0a8bc543081909afe2d159063e292 |
| moody-secret-power | 5 | $0.15 | batch_69c0a915686081909584f042f303b177 |
| moody-overcoming-life | 8 | $0.24 | batch_69c0a91721c88190b8ee61e3d0cd2a9e |
| moody-pleasure-profit | 16 | $0.48 | batch_69c0a918c8e481909444bf4a8787d2b6 |
| moody-prevailing-prayer | 12 | $0.36 | batch_69c0a91a3f188190a55f1e8f09a45f25 |
| luther-large-catechism | 15 | $0.45 | batch_69c0a91be6b08190a08cb508bd96b902 |
| luther-small-catechism | 4 | $0.12 | batch_69c0a91f11708190b88267062f158514 |
| luther-table-talk | 11 | $0.33 | batch_69c0a920443c81908423bcd24da073be |
| griffis-hermit-nation | 56 | $1.68 | batch_69c0a922ca24819092db07589153d65c |

**소계**: 136 챕터, ~$4.08

## Batch 15 — CCEL 소스 10권

| slug | 챕터 | 비용 | Batch ID |
|------|------|------|----------|
| spurgeon-all-of-grace | 5 | $0.15 | batch_69c0aac59a888190823a6125ca68b854 |
| spurgeon-checkbook-bank | 13 | $0.39 | batch_69c0aac80a2481908a58ce15918b4045 |
| owen-glory-christ | 13 | $0.39 | batch_69c0aaca31cc81909637b8999b04baae |
| owen-temptation | 10 | $0.30 | batch_69c0aacbce208190b65fbf78ca7344c0 |
| owen-indwelling-sin | 18 | $0.54 | batch_69c0aace223881908e0f68f1a91e2a83 |
| owen-communion-god | 39 | $1.17 | batch_69c0aad194f481909c83eafd7b58aa9e |
| owen-spiritual-mindedness | 25 | $0.75 | batch_69c0aad3a7488190be3b2b3711234f8c |
| watson-body-divinity-v1 | 11 | $0.33 | batch_69c0aad602ec8190b68592e1c32fb9f7 |
| watson-ten-commandments | 17 | $0.51 | batch_69c0aad7f5cc8190bb177aa89f3bcaaf |
| watson-lords-prayer | 24 | $0.72 | batch_69c0aada2e3881908642d2ffd00bdc88 |

**소계**: 175 챕터, ~$5.25

## 합계

- **총 19권, 311챕터**
- **예상 비용: ~$9.33**

## 상태 확인 명령어

```bash
# 개별 확인
.venv/bin/python -m pipeline.scripts.run_book check <slug> <batch_id>

# 전체 상태 확인
for bid in batch_69c0a8bc543081909afe2d159063e292 batch_69c0a915686081909584f042f303b177 batch_69c0a91721c88190b8ee61e3d0cd2a9e batch_69c0a918c8e481909444bf4a8787d2b6 batch_69c0a91a3f188190a55f1e8f09a45f25 batch_69c0a91be6b08190a08cb508bd96b902 batch_69c0a91f11708190b88267062f158514 batch_69c0a920443c81908423bcd24da073be batch_69c0a922ca24819092db07589153d65c batch_69c0aac59a888190823a6125ca68b854 batch_69c0aac80a2481908a58ce15918b4045 batch_69c0aaca31cc81909637b8999b04baae batch_69c0aacbce208190b65fbf78ca7344c0 batch_69c0aace223881908e0f68f1a91e2a83 batch_69c0aad194f481909c83eafd7b58aa9e batch_69c0aad3a7488190be3b2b3711234f8c batch_69c0aad602ec8190b68592e1c32fb9f7 batch_69c0aad7f5cc8190bb177aa89f3bcaaf batch_69c0aada2e3881908642d2ffd00bdc88; do
  echo "$bid:"
  .venv/bin/python -c "
from pipeline.batch.submitter import check_batch_status
s = check_batch_status('$bid')
print(f\"  {s['status']} ({s.get('completed',0)}/{s.get('total',0)})\")
"
done
```

## 결과 다운로드 명령어

```bash
# 완료 후 다운로드
.venv/bin/python -m pipeline.scripts.run_book download moody-way-to-god batch_69c0a8bc543081909afe2d159063e292
# ... (각 도서별로 실행)
```
