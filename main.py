from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from datetime import datetime

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")
static_dir = os.path.join(current_dir, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory=templates_dir)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("pages/home.html", {
        "request": request,
        "company_name": "Your Company",
        "current_year": datetime.now().year
    })

@app.get("/data-request")
async def data_request(request: Request):
    return templates.TemplateResponse("data_request.html", {
        "request": request,
        "company_name": "Your Company",
        "current_year": datetime.now().year
    })

@app.get("/databases")
async def databases(request: Request):
    return templates.TemplateResponse("databases.html", {
        "request": request,
        "company_name": "Your Company",
        "current_year": datetime.now().year
    })

if __name__ == "__main__":
    import uvicorn
    print(f"Templates directory: {templates_dir}")
    print(f"Contents of templates directory: {os.listdir(templates_dir)}")
    print(f"Contents of pages directory: {os.listdir(os.path.join(templates_dir, 'pages'))}")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)