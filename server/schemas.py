from pydantic import BaseModel, ConfigDict, HttpUrl

class WebsiteCreate(BaseModel):
    name: str
    url: HttpUrl
    username: str
    app_password: str

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["url"] = str(data["url"])
        return data

class WebsiteOut(BaseModel):
    id: int
    name: str
    url: HttpUrl
    username: str
    app_password: str

    model_config = ConfigDict(from_attributes=True)