from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
from fastapi.responses import HTMLResponse

def get_notifications(user_id):
    return [{"id": 1, "message": "새로운 알림입니다."}]

def get_notification_count(user_id):
    return len(get_notifications(user_id))

def create_app():
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
    app.templates = Jinja2Templates(directory="app/templates")
    return app

app = create_app()

def get_user_id():
    return 1

def get_dummy_data():
    user_id = get_user_id()
    notifications = get_notifications(user_id)
    return {
        'user': {"name": "John Doe", "email": "john@example.com", "profile_image": None},
        'company_name': 'Your Company',
        'current_year': datetime.now().year,
        'notification_count': len(notifications),
        'notifications': notifications,
        'team': {"name": "Team A", "image": None},
        'issue': {"title": "Sample Issue", "content": "This is a sample issue content."},
        'departments': ["HR", "IT", "Marketing"],
    }

@app.get('/')
async def home(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/home.html', {"request": request, **dummy_data})

@app.get('/404', name='error_404')
async def error_404(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/404.html', {"request": request, **dummy_data})

@app.get('/admin/settings', name='admin_settings')
async def admin_settings(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/admin_settings.html', {"request": request, **dummy_data})

@app.get('/db-info', name='db_info')
async def db_info(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/db_info.html', {"request": request, **dummy_data})

@app.get('/feed', name='feed')
async def feed(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/feed.html', {"request": request, **dummy_data})

@app.get('/profile/edit', name='profile_edit')
async def profile_edit(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/profile_edit.html', {"request": request, **dummy_data})

@app.get('/data-request', name='data_request')
async def data_request(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/data_request.html', {"request": request, **dummy_data})

@app.get('/profile', name='profile_view')
async def profile_view(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/profile_view.html', {"request": request, **dummy_data})

@app.get('/sign-in', name='sign_in')
async def sign_in(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/sign_in.html', {"request": request, **dummy_data})

@app.get('/sign-up', name='sign_up')
async def sign_up(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/sign_up.html', {"request": request, **dummy_data})

@app.get('/success', name='success')
async def success(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/success.html', {"request": request, **dummy_data})

@app.get('/team-profile/edit', name='team_profile_edit')
async def team_profile_edit(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/team_profile_edit.html', {"request": request, **dummy_data})

@app.get('/team-profile', name='team_profile_view')
async def team_profile_view(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/team_profile_view.html', {"request": request, **dummy_data})

@app.get('/issue-view', name='issue_view')
async def issue_view(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/issue_view.html', {"request": request, **dummy_data})

@app.get('/footer', name='footer')
async def footer(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/footer.html', {"request": request, **dummy_data})

@app.get('/header', name='header')
async def header(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/header.html', {"request": request, **dummy_data})

@app.get('/databases', name='databases')
async def databases(request: Request):
    dummy_data = get_dummy_data()
    return app.templates.TemplateResponse('pages/databases.html', {"request": request, **dummy_data})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)