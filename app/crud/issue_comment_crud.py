'''이슈 댓글 데이터를 CRUD하기 위한 모듈'''


import base64

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.profile import TeamProfile, PersonalProfile, TeamMembership
from app.models.issue import IssueComment
from app.models.database import datasquare_db
from app.schemas.issue import IssueCommentView


class IssueCommentData():
    '''이슈 댓글 데이터를 CRUD하는 클래스'''

    def __init__(self,
                 current_userid: str,
                 db: Session = datasquare_db
                 ) -> None:
        '''IssueCommentData 클래스의 초기화 메서드'''

        self.current_userid = current_userid
        self.db = db

    def create_issue_comment(self,
                             issue_id: int,
                             content: str
                             ) -> None:
        '''새 댓글을 생성하고 저장하는 함수'''

        new_comment = IssueComment(
            publisher=self.current_userid,
            within=issue_id,
            content=content,
            is_deleted=0
        )

        with next(self.db.get_db()) as db_session:
            db_session.add(new_comment)
            db_session.commit()
            db_session.refresh(new_comment)

    def read_issue_comment(self,
                           comment_id: int) -> IssueComment:
        '''특정 댓글 ID에 해당하는 댓글을 조회하는 함수'''

        with next(self.db.get_db()) as db_session:
            comment = db_session.query(IssueComment) \
                .filter(and_(IssueComment.comment_id == comment_id,
                             IssueComment.is_deleted == 0)) \
                .one_or_none()

        return comment

    def read_issue_comments(self,
                            issue_id: int
                            ) -> list:
        '''특정 이슈에 대한 모든 댓글을 조회하는 함수'''

        with next(self.db.get_db()) as db_session:
            comments = db_session.query(IssueComment, PersonalProfile, TeamProfile) \
                .filter(and_(IssueComment.within == issue_id,
                             IssueComment.is_deleted == 0)) \
                .outerjoin(PersonalProfile, PersonalProfile.profile_id == IssueComment.publisher) \
                .outerjoin(TeamMembership, TeamMembership.member_id == PersonalProfile.profile_id) \
                .outerjoin(TeamProfile, TeamProfile.profile_id == TeamMembership.team_id) \
                .all()

        issue_comments = []
        for issue_comment, personal_profile, team_profile in comments:
            comment = IssueCommentView(
                issue_id=issue_comment.within,
                comment_id=issue_comment.comment_id,
                publisher_id=issue_comment.publisher,
                publisher=personal_profile.name,
                team=team_profile.team_name,
                content=issue_comment.content,
                image=base64.b64encode(
                    personal_profile.profile_image).decode('utf-8')
            )
            issue_comments.append(comment)

        return issue_comments

    def modified_issue_comment(self,
                               comment_id: int,
                               content: str) -> IssueComment:
        '''특정 댓글을 수정하는 함수'''

        with next(self.db.get_db()) as db_session:
            comment = db_session.query(IssueComment) \
                .filter(IssueComment.comment_id == comment_id) \
                .one_or_none()

            if comment is None:
                return None

            if comment.publisher != self.current_userid:
                raise PermissionError(
                    "You don't have permission to modify this comment.")

            comment.content = content
            db_session.commit()
            db_session.refresh(comment)

        return comment

    def delete_all_issue_comment(self,
                                 comments_id_list: list) -> None:
        '''특정 댓글 ID 리스트에 해당하는 댓글들을 삭제하는 함수'''

        with next(self.db.get_db()) as db_session:
            for comment_id in comments_id_list:
                comment = db_session.query(IssueComment) \
                    .filter(IssueComment.comment_id == comment_id) \
                    .one_or_none()

                comment.is_deleted = 1
                db_session.commit()

            db_session.refresh(comment)

    def delete_issue_comment(self,
                             comment_id: int) -> bool:
        '''특정 댓글을 삭제하는 함수'''

        with next(self.db.get_db()) as db_session:
            comment = db_session.query(IssueComment) \
                .filter(IssueComment.comment_id == comment_id) \
                .one_or_none()

            if comment.publisher != self.current_userid:
                raise PermissionError(
                    "You don't have permission to delete this comment."
                )

            comment.is_deleted = 1
            db_session.commit()
            db_session.refresh(comment)

        return True
