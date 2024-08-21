'''issue_comment 데이터를 curd 하기 위한 파일입니다.'''


from sqlalchemy.orm import Session

from app.models.issue import IssueComment
from app.models.database import datasquare_db


class IssueCommentData():
    '''IssueCommentData crud 클래스입니다.'''

    def __init__(self,
                 current_userid: str,
                 db: Session = datasquare_db
                 ) -> None:

        self.current_userid = current_userid
        self.db = db

    def create_issue_comment(self,
                             issue_id: int,
                             content: str
                             ):
        '''
        issue_comment 데이터를 생성합니다.
        register를 통해 create_issue_comment를 오버로딩합니다.
        댓글 기능을 사용할 때 실행됩니다.
        '''

        new_comment = IssueComment(
            publisher=self.current_userid,
            within=issue_id,
            content=content
        )

        with next(self.db.get_db()) as db_session:
            db_session.add(new_comment)
            db_session.commit()
            db_session.refresh(new_comment)

    def read_issue_comment(self,
                           comment_id: int):
        '''특정 comment_id에 해당하는 댓글을 조회합니다.'''

        with next(self.db.get_db()) as db_session:
            comment = db_session.query(IssueComment).filter(
                IssueComment.id == comment_id).one_or_none()

        return comment

    def read_issue_comments(self,
                            issue_id: int
                            ):
        '''
        이슈에 해당하는 issue_comment 데이터들을 불러오는 함수입니다.
        issue_comment들을 리스트 형태로 리턴합니다.
        '''

        with next(self.db.get_db()) as db_session:
            comments = db_session.query(IssueComment) \
                .filter(IssueComment.within == issue_id) \
                .all()

        return comments

    def modified_issue_comment(self,
                               comment_id: int,
                               content: str):
        '''
        comment를 수정하는 함수입니다.
        comment_id를 받고 데이터를 수정합니다.
        '''

        with next(self.db.get_db()) as db_session:
            comment = self.read_issue_comment(comment_id=comment_id)

            if comment is None:
                return None

            if comment.publisher != self.current_userid:
                raise PermissionError(
                    "You don't have permission to modify this comment.")

            comment.content = content
            db_session.commit()
            db_session.refresh(comment)

        return comment

    def delete_issue_comment(self,
                             comment_id: int):
        '''특정 comment_id에 해당하는 댓글을 삭제합니다.'''

        with next(self.db.get_db()) as db_session:
            comment = self.read_issue_comment(comment_id=comment_id)

            if comment is None:
                return False

            if comment.publisher != self.current_userid:
                raise PermissionError(
                    "You don't have permission to delete this comment.")

            db_session.delete(comment)
            db_session.commit()

        return True
