from pydantic import BaseModel, HttpUrl

class WebsiteCreate(BaseModel):
    name: str
    url: HttpUrl
    username: str
    app_password: str

class WebsiteOut(BaseModel):
    id: int
    name: str
    url: HttpUrl
    username: str
    app_password: str

    class Config:
        orm_mode = True 