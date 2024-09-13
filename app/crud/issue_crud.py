'''이슈 데이터를 CRUD하기 위한 모듈'''


import base64

from sqlalchemy.orm import Session

from app.crud.issue_comment_crud import IssueCommentData
from app.models.profile import TeamProfile, PersonalProfile, TeamMembership
from app.models.issue import Issue
from app.models.database import datasquare_db
from app.schemas.data_request import DataRequestView
from app.utils.time import current_time


class IssueData():
    '''이슈 데이터를 CRUD하는 클래스'''

    def __init__(
        self,
            current_userid: str,
            db: Session = datasquare_db
    ) -> None:
        '''IssueData 클래스의 초기화 메서드'''

        self.current_userid = current_userid
        self.db = db

    def create_issue(
        self,
            title: str,
            content: str,
            requested_team: str,
            is_private: int
    ) -> Issue:
        '''새 이슈를 생성하고 저장하는 함수'''

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

    def read_issues_all(self) -> list[Issue]:
        '''모든 이슈를 읽어와 리스트로 반환하는 함수'''

        with next(self.db.get_db()) as db_session:
            issues = db_session.query(Issue) \
                .filter(Issue.is_deleted == 0) \
                .all()

        return issues

    def read_issue(self, issue_id: int):
        '''주어진 ID에 해당하는 이슈 데이터를 읽어오는 함수'''

        with next(self.db.get_db()) as db_session:
            issue_data = db_session \
                .query(Issue, PersonalProfile, TeamProfile) \
                .filter(Issue.issue_id == issue_id) \
                .outerjoin(PersonalProfile, Issue.publisher == PersonalProfile.profile_id) \
                .outerjoin(TeamMembership, PersonalProfile.profile_id == TeamMembership.member_id) \
                .outerjoin(TeamProfile, TeamMembership.team_id == TeamProfile.profile_id) \
                .filter(Issue.is_deleted == 0).one_or_none()

        try:
            issue_object = issue_data[0]
            personal_object = issue_data[1]
            team_object = issue_data[2]

            ret = DataRequestView(
                issue_id=issue_object.issue_id,
                title=issue_object.title,
                content=issue_object.content,
                publisher=issue_object.publisher,
                requested_team=issue_object.requested_team,
                is_private=issue_object.is_private,
                created_at=issue_object.created_at,
                modified_at=issue_object.modified_at,
                is_deleted=issue_object.is_deleted,
                publisher_name=personal_object.name,
                publisher_image=base64.b64encode(
                    personal_object.profile_image).decode('utf-8'),
                publisher_team=team_object.team_name
            )

            return ret
        except:
            return None

    def update_issue_data(
        self,
        issue_id: int,
        title: str,
        content: str,
        requested_team: str,
        is_private: int
    ) -> Issue:
        '''이슈의 내용을 수정하는 함수'''

        with next(self.db.get_db()) as db_session:
            issue = db_session.query(Issue) \
                .filter(Issue.issue_id == issue_id) \
                .one_or_none()

            if issue is None or issue.is_deleted == 1:
                return False

            issue.title = title
            issue.content = content
            issue.requested_team = requested_team
            issue.is_private = is_private
            issue.modified_at = current_time()

            db_session.commit()
            db_session.refresh(issue)

        return issue

    def delete_issue_data(self, issue_id: int) -> None:
        '''해당 이슈를 삭제하는 함수'''

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
