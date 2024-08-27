'''issue_comment schema를 정의하는 class'''


from pydantic import BaseModel


class IssueCommentView(BaseModel):
    '''Issue_comment schema'''

    issue_id: int
    comment_id: int
    publisher_id: int
    publisher: str
    team: str
    content: str
    image: str
