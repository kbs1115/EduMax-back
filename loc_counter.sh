#!/bin/bash

# 총 라인 수를 저장할 변수
total_lines=0

# 현재 디렉토리 및 모든 하위 디렉토리에서 .py 파일을 찾습니다
for file in $(find . -name "*.py"); do
    # 파일의 코드 라인 수를 계산합니다
    line_count=$(wc -l < "$file")
    echo "File: $file - Lines of code: $line_count"
    
    # 총 라인 수에 추가합니다
    total_lines=$((total_lines + line_count))
done

# 모든 .py 파일의 총 라인 수를 출력합니다
echo "Total lines of code in all .py files: $total_lines"

