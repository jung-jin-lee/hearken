#!/bin/bash
# 14권 신규 도서 배치 상태 확인 & 다운로드 스크립트
# 사용법: bash pipeline/scripts/check_batch14.sh [check|download]

declare -A BATCHES
BATCHES[christian-secret]="batch_69bfd5b0a08881909c190cb9de3cb50b"
BATCHES[power-through-prayer]="batch_69bfd5bed2c08190acd636efd89c1ad5"
BATCHES[on-loving-god]="batch_69bfd5c0c8688190991400d739de223a"
BATCHES[short-method-prayer]="batch_69bfd5c2536081908c46402abfeb8c54"
BATCHES[story-of-a-soul]="batch_69bfd5c4773c8190857f95ba7ecbbe54"
BATCHES[keeping-the-heart]="batch_69bfd5c633a88190bb2ab488af5a5ab2"
BATCHES[revelations-divine-love]="batch_69bfd5c7dc908190beb19dd24301389c"
BATCHES[mueller-autobiography]="batch_69bfd5ca702481908c6f1930e41b1ce9"
BATCHES[wesley-sermons]="batch_69bfd5cd1f8481908bb8d8cbd56a5fcb"
BATCHES[cloud-of-unknowing]="batch_69bfd5cf3ea881909c9a6bca58bcf646"
BATCHES[chrysostom-homilies]="batch_69bfd5d1107c81908e19ea3c81c88b0b"
BATCHES[watson-beatitudes]="batch_69bfd5d4a6d48190aaf032f1e5d4d803"
BATCHES[dialogue-catherine]="batch_69bfd5d70108819090ebf14386dfab0c"
BATCHES[passion-of-perpetua]="batch_69bfd5d8b3388190b1969262d1dc2109"

ACTION="${1:-check}"

for slug in "${!BATCHES[@]}"; do
  bid="${BATCHES[$slug]}"
  if [ "$ACTION" = "download" ]; then
    echo "===== DOWNLOAD: $slug ====="
    .venv/bin/python -m pipeline.scripts.run_book download "$slug" "$bid"
  else
    echo -n "$slug: "
    .venv/bin/python -m pipeline.scripts.run_book check "$slug" "$bid" 2>&1 \
      | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['status'])" 2>/dev/null \
      || echo "error"
  fi
done
