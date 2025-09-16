from apscheduler.schedulers.background import BackgroundScheduler
from crawler import crawl_single_site, crawl_sites
from database import SessionLocal, engine, Base
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Website, CrawlResult
from schemas import CrawlResultOut, WebsiteCreate, WebsiteOut
from sqlalchemy import desc
from sqlalchemy.orm import Session
from typing import List

import logging
import os

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path='/api')

origins = [
    os.environ.get('CLIENT_URL', 'http://localhost:5173')
]

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_website_by_id(website_id: int, db: Session) -> Website:
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail='Website not found')
    return website

@app.get('/v1/websites', response_model=List[WebsiteOut])
def read_websites(db: Session = Depends(get_db)):
    websites = db.query(Website).all()

    for website in websites:
        latest_crawl = (
            db.query(CrawlResult)
            .filter(CrawlResult.website_id == website.id)
            .order_by(desc(CrawlResult.timestamp))
            .first()
        )
        website.latest_crawl = latest_crawl

    return websites

@app.post('/v1/websites')
def create_website(website: WebsiteCreate, db: Session = Depends(get_db)):
    db_website = Website(
        name=website.name,
        url=str(website.url),
        api_key=website.api_key
    )

    db.add(db_website)
    db.commit()
    db.refresh(db_website)

    crawl_single_site(db, db_website)

    return db_website

@app.get('/v1/websites/{website_id}', response_model=WebsiteOut)
def get_website(website_id: int, db: Session = Depends(get_db)):
    website = get_website_by_id(website_id, db)

    latest_crawl = (
        db.query(CrawlResult)
        .filter(CrawlResult.website_id == website.id)
        .order_by(desc(CrawlResult.timestamp))
        .first()
    )

    website.latest_crawl = latest_crawl

    return website

@app.put('/v1/websites/{website_id}', response_model=WebsiteOut)
def update_website(website_id: int, updated: WebsiteCreate, db: Session = Depends(get_db)):
    db_website = get_website_by_id(website_id, db)

    db_website.name = updated.name
    db_website.url = str(updated.url)
    db_website.api_key = updated.api_key
    db_website.maintainers = updated.maintainers
    db_website.comments = updated.comments

    db.commit()
    db.refresh(db_website)

    crawl_single_site(db, db_website)

    return db_website

@app.delete('/v1/websites/{website_id}', status_code=204)
def delete_website(website_id: int, db: Session = Depends(get_db)):
    website = get_website_by_id(website_id, db)
    db.delete(website)
    db.commit()
    return

@app.get('/v1/crawl-results/{website_id}', response_model=List[CrawlResultOut])
def get_crawl_results(website_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(CrawlResult)
        .filter(CrawlResult.website_id == website_id)
        .order_by(CrawlResult.timestamp.desc())
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail='No crawl results found for this website')

    return results

# APScheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(crawl_sites, 'interval', minutes=15)
scheduler.start()

@app.on_event('shutdown')
def shutdown_event():
    scheduler.shutdown()