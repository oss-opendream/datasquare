import base64

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.models.database import Base, SessionLocal, engine
from app.models.issue import Issue, PersonalProfile

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

    issue_data = []

    for issue in issues:
        author = issue.publisher

        issue_data.append({
            "title": issue.title,
            "content": issue.content,
            "author_name": author.name,
            # "team": author.memberships.team_id,
            "profile_pic": base64.b64encode(author.profile_image).decode("utf-8")
        })

    # return issues
    return templates.TemplateResponse("feed.html", {"request": request, "issues": issue_data})


@router.get("/feed/my_issues")
async def read_my_issues(request: Request, db: Session = Depends(get_db)):
    # 'author_id='에 로그인 유저 ID 값 입력 필요(예시 ID: 1)
    my_issues = db.query(Issue).filter_by(publisher_id=1).all()

    issue_data = []

    for issue in my_issues:
        author = issue.publisher

        issue_data.append({
            "title": issue.title,
            "content": issue.content,
            "author_name": author.name,
            # "team": author.memberships.team_id,
            "profile_pic": base64.b64encode(author.profile_image).decode("utf-8")
        })

    return templates.TemplateResponse("feed.html", {"request": request, "issues": issue_data})


@router.get("/feed/search")
async def search_issues(request: Request, query: str, db: Session = Depends(get_db)):
    search_result = db.query(Issue).filter(
        Issue.title.contains(query)).all()

    result_data = []

    for issue in search_result:
        author = issue.publisher

        result_data.append({
            "title": issue.title,
            "content": issue.content,
            "author_name": author.name,
            # "team": author.memberships.team_id,
            "profile_pic": base64.b64encode(author.profile_image).decode("utf-8")
        })

    return templates.TemplateResponse("feed.html", {"request": request, "issues": result_data})
