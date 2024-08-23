#! /bin/bash

set -e

# pip install -r ./requirements.txt
python3 ./app/utils/key_scribe.py "$@"
fastapi run 