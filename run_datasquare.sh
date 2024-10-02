#! /bin/bash

# 실행이 실패하면 다음 명령어로 가지 않고 종료되도록 설정
set -e

/root/.local/share/pypoetry/venv/bin/poetry install 
python3 ./app/utils/key_scribe.py "$@"
/root/.local/share/pypoetry/venv/bin/poetry run fastapi run 