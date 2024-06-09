from sqlmodel import Field, SQLModel
from pydantic import HttpUrl


class BaseLINEUser(SQLModel):
    user_id: str 
    display_name: str
    picture_url: HttpUrl | None = None
    status_message: str | None = None
    language: str | None = None


class LINEUser(BaseLINEUser, table=True):
    user_id: str = Field(primary_key=True)