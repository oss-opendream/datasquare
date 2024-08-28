'''data_request schema를 정의하는 class'''


from pydantic import BaseModel


class DataRequestCreate(BaseModel):
    '''data request create class'''

    issue_id: int
    title: str
    content: str
    publisher: int
    requested_team: int
    is_private: int
    created_at: str
    modified_at: str
    is_deleted: int


class DataRequestView(DataRequestCreate):
    ''' data request view class'''

    publisher_name: str
    publisher_image: str
    publisher_team: str
