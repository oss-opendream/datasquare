from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.models.database import Base, SessionLocal, engine
from app.models.issue import Issue

Base.metadata.create_all(bind=engine)

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/feed")
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    issues = db.query(Issue).filter_by(is_private=0).all()
    # return issues
    return templates.TemplateResponse("feed.html", {"request": request, "issues": issues})


@router.get("/feed/my_issues")
async def read_my_issues(request: Request, db: Session = Depends(get_db)):
    my_issues = db.query(Issue).filter_by(
        publisher=1).all()  # 'author_id='에 로그인 유저 ID 값 입력 필요(예시 ID: 1)
    return templates.TemplateResponse("feed.html", {"request": request, "issues": my_issues})


@router.get("/feed/search")
async def search_issues(request: Request, query: str, db: Session = Depends(get_db)):
    search_result = db.query(Issue).filter_by(
        Issue.title.contains(query)).all()
    return templates.TemplateResponse("feed.html", {"request": request, "issues": search_result})
