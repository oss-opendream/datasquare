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
from app.utils.get_current_user import get_current_user
from app.crud.noti import get_notification_count


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.post('/issue_comment/create')
async def create_issue_comment(issue_id: int = Form(...),
                               comment: str = Form(...),
                               current_user: User = Depends(get_current_user)):
    '''issue_commnet 생성 함수 입니다.'''

    IssueCommentData(current_user.profile_id).create_issue_comment(
        issue_id, comment)

    ret = RedirectResponse(
        url=f'/issue/view?issue_id={issue_id}', status_code=303)

    return ret


@router.get('/issue/view', response_class=HTMLResponse, name='issue_views')
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

    # if not comments:
    #     raise HTTPException(status_code=404, detail='Issue_Comments not found')

    ret = templates.TemplateResponse(
        'pages/issue_view.html',
        {
            'request': request,
            'issue': issue,
            'comments': comments,
            'current_user': current_user,
            'notification_count': get_notification_count(current_user.profile_id)
        }
    )

    return ret

@router.post('/issue_comment/delete')
async def delete_issue_comment(issue_id: int = Form(...),
                                comment_id: int = Form(...),
                                current_user: User = Depends(get_current_user)):
    '''issue_commnet 삭제 함수 입니다.'''

    IssueCommentData(current_userid=current_user.profile_id).delete_issue_comment(comment_id)

    ret = RedirectResponse(
        url=f'/issue/view?issue_id={issue_id}', status_code=303)

    return ret


@router.post('/issue_comment/modify')
async def modify_issue_comment(comment_id: int = Form(...),
                               content: str = Form(...),
                               current_user: User = Depends(get_current_user)):
    '''issue_comment 수정 함수입니다.'''
    
    comment = IssueCommentData(current_userid=current_user.profile_id).modified_issue_comment(comment_id=comment_id, content=content)

    issue_id = comment.within

    ret = RedirectResponse(
        url=f'/issue/view?issue_id={issue_id}', status_code=303)

    return ret