'''
issue_id를 기준으로 issue데이터와 issue_comment를 불러옵니다.
댓글을 등록하면 issue_comment를 생성하고 추가로 출력합니다.
'''


from fastapi import APIRouter, Request, HTTPException, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse


from app.crud.issue_crud import IssueData
from app.crud.issue_comment_crud import IssueCommentData
from app.schemas.user_schema import User
from app.routers.sign import get_current_user


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


# @router.post('/issue/view/create_issue_comment', response_class=HTMLResponse)
# async def create_issue_comment(issue_id: int,
#                                content: str = Form(...),
#                                current_user: User = Depends(get_current_user)):
#     '''
#     issue_commnet 생성 함수 입니다.
#     '''

#     ###
#     user_id = 1
#     ###
#     print(issue_id)
#     print(content)
#     IssueCommentData(user_id).create_issue_comment(issue_id, content)

#     return RedirectResponse(url=f'/issue/view/issue_id={issue_id}', status_code=303)


@router.get('/issue/view', response_class=HTMLResponse)
async def issue_views(request: Request,
                      issue_id: int,
                      current_user: User = Depends(get_current_user)
                      ):
    '''
    이슈 조회 함수입니다.
    issue_id를 기준으로 issue 데이터와
    issue_comment.within == issue.issue_id인 issue_comment데이터를 불러옵니다.
    '''

    issue = IssueData(current_user.profile_id).read_issue(issue_id)

    if not issue:
        raise HTTPException(status_code=404, detail='Issue not found')

    comments = IssueCommentData(
        current_user.profile_id).read_issue_comments(issue_id)

    if not comments:
        raise HTTPException(status_code=404, detail='Issue_Comments not found')

    return templates.TemplateResponse('issue_view.html',
                                      {
                                          'request': request, 
                                          'issue': issue, 
                                          'comments': comments,
                                      }
    )
