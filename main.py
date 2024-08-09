from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/")
async def home(request: Request):
    try:
        return templates.TemplateResponse("pages/home.html", {
            "request": request,
            "company_name": "Your Company",
            "current_year": datetime.now().year
        })
    except Exception as e:
        print(f"Error: {e}")
        raise

@app.get("/data-request")
async def data_request(request: Request):
    return templates.TemplateResponse("pages/data_request.html", {
        "request": request,
        "company_name": "Your Company",
        "current_year": datetime.now().year
    })

@app.get("/databases")
async def databases(request: Request):
    return templates.TemplateResponse("pages/databases.html", {
        "request": request,
        "company_name": "Your Company",
        "current_year": datetime.now().year
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)