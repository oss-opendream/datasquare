'''issue 데이터를 curd 하기 위한 파일입니다.'''


from fastapi import Form
from sqlalchemy import and_
from sqlalchemy.orm import Session


from app.crud.issue_comment_crud import IssueCommentData
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
            is_deleted=0,
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
            issues = db_session.query(Issue) \
                .filter(Issue.is_deleted == 0).all()

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
                .filter(and_(Issue.issue_id == issue_id,
                             Issue.is_deleted == 0)) \
                .one_or_none()

        return issue

    def modified_issue(self,
                       issue_id: int = Form(...),
                       title: str = Form(...),
                       content: str = Form(...),
                       requested_team: str = Form(...),
                       is_private: int = Form(...)
                       ):
        '''
        issue 내용을 수정하는 함수입니다.
        issue_id를 받아서 해당 이슈를 수정합니다.
        '''

        with next(self.db.get_db()) as db_session:
            issue = db_session.query(Issue) \
                .filter(Issue.issue_id == issue_id) \
                .one_or_none()

            if issue is None or issue.is_deleted == 1:
                return False

        # 수정할 필드 업데이트
            issue.title = title
            issue.content = content
            issue.requested_team = requested_team
            issue.is_private = is_private
            issue.modified_at = current_time()

            db_session.commit()
            db_session.refresh(issue)

        return issue

    def delete_issue(self,
                     issue_id: int):
        '''
        issue를 삭제하는 함수입니다.
        issue_id를 받아서 해당 이슈를 삭제합니다.
        '''

        with next(self.db.get_db()) as db_session:
            issue = db_session.query(Issue) \
                .filter(Issue.issue_id == issue_id) \
                .one_or_none()

            issue_comment_data = IssueCommentData(self.current_userid)
            comments = issue_comment_data.read_issue_comments(
                issue_id=issue_id)
            comments_id_list = [comment.comment_id for comment in comments]
            issue_comment_data.delete_all_issue_comment(comments_id_list)

            if issue is None or issue.is_deleted == 1:
                raise ValueError("Issue is None")

            if issue.publisher != self.current_userid:
                raise PermissionError(
                    "You don't have permission to delete this comment."
                )
            issue.is_deleted = 1
            issue.modified_at = current_time()

            db_session.commit()
            db_session.refresh(issue)

        return True
