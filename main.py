from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))
app.mount('/static', StaticFiles(directory=str(BASE_DIR / 'static')), name='static')

def get_notification_count(user_id):
    return 5  # 임시로 5개의 알림이 있다고 가정

def get_notifications(user_id: int):
    # 이 함수는 실제로 데이터베이스에서 알림을 가져와야 합니다.
    # 여기서는 예시로 더미 데이터를 반환합니다.
    return [
        {"message": "새로운 데이터 요청이 있습니다."},
        {"message": "데이터베이스가 업데이트되었습니다."}
    ]

@app.get('/', name='home')
async def home(request: Request):
    user_id = 1  # 예시 사용자 ID
    notifications = get_notifications(user_id)
    notification_count = len(notifications)
    return templates.TemplateResponse('pages/home.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': notification_count,
        'notifications': notifications
    })


@app.get('/data-request', name='data_request')
async def data_request(request: Request):
    user_id = 1
    notification_count = get_notification_count(user_id)
    return templates.TemplateResponse('pages/data_request.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': notification_count
    })

@app.get('/databases', name='databases')
async def databases(request: Request):
    user_id = 1
    notification_count = get_notification_count(user_id)
    return templates.TemplateResponse('pages/databases.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': notification_count
    })
@app.get('/api/notifications')
async def api_notifications(request: Request):
    # 실제 구현에서는 현재 로그인한 사용자의 ID를 사용해야 합니다.
    user_id = 1  
    notifications = get_notifications(user_id)
    return {"notifications": notifications}

@app.get('/api/notification-count')
async def api_notification_count(request: Request):
    user_id = 1  # 실제 구현에서는 현재 로그인한 사용자의 ID를 사용해야 합니다.
    notification_count = get_notification_count(user_id)
    return {"count": notification_count}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)