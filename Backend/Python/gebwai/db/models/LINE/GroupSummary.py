from pydantic import HttpUrl
from sqlmodel import SQLModel


class GroupSummary(SQLModel):
    """
    https://developers.line.biz/en/reference/messaging-api/#get-group-summary
    """

    group_id: str
    group_name: str
    picture_url: HttpUrl | None = None
