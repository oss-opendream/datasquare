'''issue 데이터를 curd 하기 위한 파일입니다.'''


from functools import singledispatch

from fastapi import Form
from sqlalchemy.orm import Session

from app.models.issue import Issue
from app.models.database import datasquare_db
from app.utils.time import current_time


class IssueData():
    '''IssueData crud 클래스입니다.'''

    def __init__(self,
                 current_userid: str,
                 db: Session = datasquare_db
                 ) -> None:

        self.current_userid = current_userid
        self.db = db

    def create_issue(self,
                     title: str = Form(...),
                     content: str = Form(...),
                     requested_team: str = Form(...),
                     is_private: int = Form(...)
                     ):
        '''issue 데이터를 생성, 저장합니다.'''

        now = current_time()
        
        new_issue = Issue(
            title=title,
            content=content,
            publisher=self.current_userid,
            requested_team=requested_team,
            is_private=is_private,
            created_at=now,
            modified_at=now
            )

        with next(self.db.get_db()) as db_session:
            db_session.add(new_issue)
            db_session.commit()
            db_session.refresh(new_issue)

        return new_issue

    def read_issues_all(self):
        '''
        모든 Issue 데이터를 읽어오는 함수입니다.
        모든 Issue들을 list형태로 반환합니다.
        '''

        with next(self.db.get_db()) as db_session:
            issues = db_session.query(Issue).all()

        return issues

    def read_issue(self,
                   issue_id: int
                   ):
        '''
        Issue 데이터를 읽어오는 함수입니다.
        issue_id에 해당하는 한 개의 이슈 데이터를 읽어옵니다.
        '''

        with next(self.db.get_db()) as db_session:
            issue = db_session.query(Issue) \
                .filter(Issue.issue_id == issue_id) \
                .one_or_none()

        return issue
