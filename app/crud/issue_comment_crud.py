'''
issue_comment 데이터를 curd 하기 위한 파일입니다.
'''


from functools import singledispatch

from sqlalchemy.orm import Session

from app.models.issue import Issue, IssueComment
from app.models.database import datasquare_db


class IssueCommentData():
    '''IssueCommentData crud 클래스입니다.'''

    def __init__(self,
                 current_userid: str,
                 db: Session = datasquare_db
                 ) -> None:

        self.current_userid = current_userid
        self.db = db

    @singledispatch
    def create_issue_comment(self,
                             issue_id: int
                             ):
        '''
        issue_comment 데이터를 생성합니다.
        singledispatch를 사용하여 오버로딩을 구현합니다.
        issue를 처음 만들때 실행됩니다.
        '''

        new_comment = IssueComment(
            publisher=self.current_userid,
            within=issue_id,
            content='Init new issue!!!!'
        )

        with next(self.db.get_db()) as db_session:
            db_session.add(new_comment)
            db_session.commit()
            db_session.refresh(new_comment)

    @create_issue_comment.register
    def _(self,
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
