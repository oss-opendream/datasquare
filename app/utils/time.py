'''현재 시각 및 시간대를 처리하는 모듈'''


from datetime import datetime

import pytz


def get_timezone_code(offset):
    '''UTC 오프셋을 알파벳으로 변환하는 함수'''

    offset_hours = int(offset[:3])
    return 'YXWVUTSRQPONZABCDEFGHIKLM'[offset_hours + 12]


def current_time(timezone='Asia/Seoul'):
    '''특정 시간대의 현재 시간을 문자열 형태로 반환하는 함수'''

    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    offset = now.strftime('%z')
    timezone_code = get_timezone_code(offset)

    return now.strftime(f'%Y-%m-%dT%H:%M:%S{timezone_code}')
