## Poetry 설치 방법:

- macOS, Linux, WSL 환경:
```curl -sSL https://install.python-poetry.org | python3 -```
1. 위 명령어 실행 후 출력되는 PATH 설정 문구를 ~/.zshrc 또는 ~/.bashrc에 붙여넣기 후 저장
2. source ~/.zshrc 또는 source ~/.bashrc 명령어 실행
3. poetry --version 명령 실행 시, Poetry 버전 출력 확인

## Windows(PowerShell) 환경:
```(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -```
4. 위 명령어 실행 후 환경변수에 %APPDATA%\pypoetry\venv\Scripts\poetry 등록
5. poetry --version 명령 실행 시, Poetry 버전 출력 확인


## Poetry를 통한 의존성 패키지 설치 및 fastapi 실행 방법:

6. 터미널에서 datasquare 디렉터리로 이동
7. poetry install 실행
8. poetry run fastapi run 또는 poetry run fastapi dev 명령어 실행
