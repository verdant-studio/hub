from datetime import datetime
from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import List, Optional

class SubSite(BaseModel):
    site_id: str
    site_url: HttpUrl
    site_name: str

class CrawlResultOut(BaseModel):
    id: int
    status_code: Optional[int]
    response_time_ms: Optional[int]
    timestamp: datetime

    wp_version: Optional[str]
    health_rating: Optional[int]
    updates_available: Optional[int]
    multisite: Optional[bool] = None
    subsites: Optional[List[SubSite]] = None

    model_config = ConfigDict(from_attributes=True)

class WebsiteCreate(BaseModel):
    name: str
    url: HttpUrl
    username: str
    app_password: str
    maintainers: Optional[str] = None
    comments: Optional[str] = None

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
    maintainers: Optional[str] = None
    comments: Optional[str] = None
    latest_crawl: Optional[CrawlResultOut] = None

    model_config = ConfigDict(from_attributes=True)