from sqlalchemy import Column, Integer, String
from database import Base

class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    username = Column(String, nullable=False)
    app_password = Column(String, nullable=False)