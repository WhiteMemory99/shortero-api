from pydantic import BaseModel, Field, HttpUrl


class OutLink(BaseModel):
    original_url: HttpUrl
    clicks: int = Field(ge=0)

    class Config:
        orm_mode = True
