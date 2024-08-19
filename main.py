from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime
from fastapi import HTTPException

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def get_notification_count(user_id):
    return 5  # 임시로 5개의 알림이 있다고 가정

def get_notifications(user_id: int):
    return [
        {"message": "새로운 데이터 요청이 있습니다."},
        {"message": "데이터베이스가 업데이트되었습니다."}
    ]

@app.get('/')
async def home(request: Request):
    try:
        user_id = 1
        notifications = get_notifications(user_id)
        notification_count = len(notifications)
        return templates.TemplateResponse('pages/home.html', {
            'request': request,
            'company_name': 'Your Company',
            'current_year': datetime.now().year,
            'notification_count': notification_count,
            'notifications': notifications
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get('/profile', name='profile_view')
async def profile_view(request: Request):
    user_id = 1
    notification_count = get_notification_count(user_id)
    return templates.TemplateResponse('pages/profile_view.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': notification_count,
        'user': {'name': 'John Doe', 'email': 'john@example.com', 'department': 'IT', 'phone': '123-456-7890'}
    })

@app.get('/team-profile', name='team_profile_view')
async def team_profile_view(request: Request):
    user_id = 1
    notification_count = get_notification_count(user_id)
    return templates.TemplateResponse('pages/team_profile_view.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': notification_count,
        'team': {'name': 'IT Team', 'members': [{'name': 'John Doe'}, {'name': 'Jane Smith'}]}
    })

@app.get('/sign-in', name='sign_in')
async def sign_in(request: Request):
    return templates.TemplateResponse('pages/sign_in.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year
    })

@app.get('/api/notifications')
async def api_notifications(request: Request):
    user_id = 1
    notifications = get_notifications(user_id)
    return {"notifications": notifications}

@app.get('/api/notification-count')
async def api_notification_count(request: Request):
    user_id = 1
    notification_count = get_notification_count(user_id)
    return {"count": notification_count}

@app.get('/profile/edit', name='profile_edit')
async def profile_edit(request: Request):
    user_id = 1
    notification_count = get_notification_count(user_id)
    return templates.TemplateResponse('pages/profile_edit.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': notification_count,
        'user': {'name': 'John Doe', 'email': 'john@example.com', 'department': 'IT', 'phone': '123-456-7890'},
        'departments': [{'id': 1, 'name': 'IT'}, {'id': 2, 'name': 'HR'}]
    })

@app.get('/team-profile/edit', name='team_profile_edit')
async def team_profile_edit(request: Request):
    user_id = 1
    notification_count = get_notification_count(user_id)
    return templates.TemplateResponse('pages/team_profile_edit.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': notification_count,
        'team': {'name': 'IT Team', 'members': [{'name': 'John Doe'}, {'name': 'Jane Smith'}]},
        'all_users': [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]
    })

@app.get('/admin/settings', name='admin_settings')
async def admin_settings(request: Request):
    user_id = 1
    notification_count = get_notification_count(user_id)
    return templates.TemplateResponse('pages/admin_settings.html', {
        'request': request,
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': notification_count,
        'teams': [{'name': 'IT Team', 'admin': {'name': 'John Doe'}}, {'name': 'HR Team', 'admin': {'name': 'Jane Smith'}}]
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)