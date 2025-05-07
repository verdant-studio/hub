from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class CrawlResult(Base):
    __tablename__ = 'crawl_results'

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey('websites.id'), nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    wp_version = Column(String, nullable=True)
    health_rating = Column(Integer, nullable=True)
    updates_available = Column(Integer, nullable=True)

    website = relationship('Website', back_populates='crawl_results')

class Website(Base):
    __tablename__ = 'websites'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    username = Column(String, nullable=False)
    app_password = Column(String, nullable=False)

    crawl_results = relationship('CrawlResult', back_populates='website', cascade='all, delete')