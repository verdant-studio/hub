from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Website
from schemas import WebsiteCreate, WebsiteOut
from database import SessionLocal, engine, Base
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or 3000 depending on Vue setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/api/v1/websites', response_model=List[WebsiteOut])
def read_websites(db: Session = Depends(get_db)):
    return db.query(Website).all()

@app.post('/api/v1/websites')
def create_website(website: WebsiteCreate, db: Session = Depends(get_db)):
    db_website = Website(**website.dict())
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    return db_website