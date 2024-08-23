#! /bin/bash

# 실행이 실패하면 다음 명령어로 가지 않고 종료되도록 설정
set -e

# pip install -r ./requirements.txt
python3 ./app/utils/key_scribe.py "$@"
fastapi run 