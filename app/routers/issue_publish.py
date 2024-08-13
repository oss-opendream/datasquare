"""
Library
"""
from datetime import date, datetime, timezone, timedelta

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.models.database import Base, engine, SessionLocal
from app.models.issue import Issue


Base.metadata.create_all(bind=engine)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/issue/publish/submit", response_class=HTMLResponse)
async def create_issue(request: Request,
                       title: str = Form(...),
                       content: str = Form(...),
                       requested_team: str = Form(...),
                       is_private: int = Form(...),
                       db: Session = Depends(get_db)
                       ):
    ###
    # test user_id
    user_id = "1"
    ###
    tz = timezone(timedelta(hours=9))
    current_time = datetime.now(tz=tz).strftime("%Y-%m-%d-%H:%M:%S")

    new_issue = Issue(
        title=title,
        content=content,
        publisher_id=user_id,
        requested_team=requested_team,
        is_private=is_private,
        created_at=current_time,
        modified_at=current_time
    )
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    issue = db.query(Issue).all()
    return templates.TemplateResponse(
        "issue_publish.html", {"request": request, "issues": issue}
    )


@router.get("/issue/publish", response_class=HTMLResponse)
async def issue_pulish(request: Request, db: Session = Depends(get_db)):
    """
    이슈 발행 함수입니다.
    """
    issues = db.query(Issue).all()
    return templates.TemplateResponse("issue_publish.html", {"request": request, "issues": issues})
