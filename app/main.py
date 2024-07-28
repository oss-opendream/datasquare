import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def read_root():
    return {'hello': 'world'}

@app.get("/feed")
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    issues = db.query(models.Issue).all()
    return templates.TemplateResponse("feed.html", {"request": request, "issues": issues})

@app.get("/feed/my_issues")
async def read_my_issues(request: Request, db: Session = Depends(get_db)):
    my_issues = db.query(models.Issue).filter_by(author_id={{"my_id"}}).all()
    return templates.TemplateResponse("feed.html", {"request": request, "issues": my_issues})

@app.get("/feed/search")
async def search_issues(request: Request, query: str, db: Session = Depends(get_db)):
    search_result = db.query(models.Issue).filter(models.Issue.title.contains(query)).all()
    return templates.TemplateResponse("feed.html", {"request": request, "issues": search_result})

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=80, reload=True)