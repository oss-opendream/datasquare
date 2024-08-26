'''서비스 인증용 secret_key를 생성, 조회하는 모듈'''


import argparse
import secrets


def parse_argeuments():
    '''shell 파일에서 args를 받아올 수 있게 하는 함수'''

    parser = argparse.ArgumentParser(description="Run DataSquare")
    parser.add_argument("--token_time", type=int, default=24,
                        help="Token expiration duration in hours. The default value is 24 hours")
    valid_algorithms = ['HS256', 'HS384', 'HS512', 'RS256', 'RS384',
                        'RS512', 'ES256', 'ES384', 'ES512', 'PS256', 'PS384', 'PS512']
    parser.add_argument("--algorithm", type=str, default="HS256", choices=valid_algorithms,
                        help='''
                        Choose a hashing algorithm for JWT from the following: 
                        HS256, HS384, HS512, RS256, RS384, RS512, ES256, ES384, ES512, PS256, PS384, PS512
                        ''')

    return parser.parse_args()


def create_key(token_time, algorithm):
    '''".env" 파일에 secret_key와 token 유효기간을 저장하는 함수'''

    with open(".env", "w", encoding="utf-8") as f:
        secret_key = secrets.token_hex(32)
        f.write(f'''ACCESS_TOKEN_EXPIRE_MINUTES={token_time}
SECRET_KEY={secret_key}
ALGORITHM={algorithm}
''')


if __name__ == "__main__":
    args = parse_argeuments()
    create_key(args.token_time, args.algorithm)
