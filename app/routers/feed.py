from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models.database import Base, engine, get_db
from app.schemas.issue import Issue

router = APIRouter()
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


@router.get("/feed")
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    issues = db.query(Issue).all()
    return templates.TemplateResponse("static/feed.html", {"request": request, "issues": issues})


@router.get("/feed/my_issues")
async def read_my_issues(request: Request, db: Session = Depends(get_db)):
    my_issues = db.query(Issue).filter_by(
        author_id={{"my_id"}}).all()  # 'author_id='에 로그인 유저 ID 값 입력 필요
    return templates.TemplateResponse("static/feed.html", {"request": request, "issues": my_issues})


@router.get("/feed/search")
async def search_issues(request: Request, query: str, db: Session = Depends(get_db)):
    search_result = db.query(Issue).filter(
        Issue.title.contains(query)).all()
    return templates.TemplateResponse("static/feed.html", {"request": request, "issues": search_result})
