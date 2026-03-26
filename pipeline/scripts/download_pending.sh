#!/bin/bash
# Batch 19-20 잔여 다운로드 스크립트
# 사용법: .venv/bin/python 경로로 실행
# ./pipeline/scripts/download_pending.sh

PYTHON=".venv/bin/python"

pairs=(
  "chesterton-father-brown-v1 batch_69c141bd806c81909a1b65714c419246"
  "livingstone-travels batch_69c141c33b7c819099122727e8161a81"
  "paton-autobiography batch_69c141c5d22c8190983ac92a2efc24ef"
  "meyer-way-into-holiest batch_69c141c8e6f081908703a18f9ba725b0"
  "flavel-fountain-life batch_69c141ccfc98819092d8cae5026e1ab1"
  "flavel-method-grace batch_69c141d033988190bd10531a45cfeea2"
  "athanasius-life-antony batch_69c141d728248190a65ab524b4dd1599"
  "gregory-naz-theological batch_69c143e6785c8190a1ef07417a9604f5"
  "augustine-enchiridion batch_69c143eaadd48190a72a45da3a825ab6"
  "chrysostom-matthew-select batch_69c143ef65fc819096c5f8d93df4be49"
  "ambrose-select batch_69c143f342408190860c86f5f947bfc7"
  "leo-gregory-great batch_69c143f6c6a8819098caad42c8d58761"
  "chesterton-father-brown-v2 batch_69c143f8b8648190b1a1ce7059525c82"
  "pascal-provincial-letters batch_69c143fa8de88190b7e8e649094f538d"
  "tolstoy-kingdom-god batch_69c143fd4a90819094311d097185121b"
  "carey-enquiry batch_69c14400616c8190a4fff73c3bdd7b7c"
  "taylor-spiritual-secret batch_69c14402193c819089bb7d2f6ac26bfd"
)

echo "=== Batch 19-20 다운로드 ==="
completed=0
failed=0

for pair in "${pairs[@]}"; do
  slug=$(echo "$pair" | cut -d' ' -f1)
  bid=$(echo "$pair" | cut -d' ' -f2)

  # Check if already downloaded
  if [ -d "content/books/$slug" ] && [ "$(ls content/books/$slug/*.json 2>/dev/null | wc -l)" -gt 0 ]; then
    echo "✅ $slug (이미 완료)"
    completed=$((completed+1))
    continue
  fi

  # Check status
  status=$($PYTHON -c "
from pipeline.batch.submitter import check_batch_status
s=check_batch_status('$bid')
print(s['status'])
" 2>/dev/null)

  if [ "$status" = "completed" ]; then
    echo "📥 $slug 다운로드 중..."
    $PYTHON -m pipeline.scripts.run_book download "$slug" "$bid" 2>&1 | grep "\[결과\]"
    completed=$((completed+1))
  else
    echo "🔄 $slug ($status)"
    failed=$((failed+1))
  fi
done

echo ""
echo "완료: $completed, 대기: $failed"
