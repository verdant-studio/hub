from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal, engine, Base
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Website, CrawlResult
from schemas import CrawlResultOut, WebsiteCreate, WebsiteOut
from sqlalchemy import delete, desc, select
from sqlalchemy.orm import Session
from typing import List

import httpx
import logging
import time

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],  # or 3000 depending on Vue setup
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

def prune_old_crawls(db: Session, website_id: int, keep: int = 5):
        # Get the IDs to delete — entries older than the most recent `keep`
    subquery = (
        select(CrawlResult.id)
        .where(CrawlResult.website_id == website_id)
        .order_by(CrawlResult.timestamp.desc())
        .offset(keep)
    ).subquery()

    # Now delete entries that match those IDs
    db.execute(
        delete(CrawlResult).where(CrawlResult.id.in_(select(subquery.c.id)))
    )
    db.commit()

def crawl_sites():
    db: Session = SessionLocal()
    websites = db.query(Website).all()

    if not websites:
      print("No websites to crawl.")
      db.close()
      return

    for site in websites:
        try:
            start = time.time()
            response = httpx.get(site.url, timeout=10)
            duration = int((time.time() - start) * 1000)

            result = CrawlResult(
                website_id=site.id,
                status_code=response.status_code,
                response_time_ms=duration,
                timestamp=datetime.utcnow()
            )
            db.add(result)
            logging.info(f'Crawled {site.url} - {response.status_code} ({duration}ms)')

        except Exception as e:
            logging.error(f'Failed to crawl {site.url}: {e}')
            result = CrawlResult(
                website_id=site.id,
                status_code=None,
                response_time_ms=None,
                timestamp=datetime.utcnow()
            )
            db.add(result)

    db.commit()
    prune_old_crawls(db, site.id, keep=5)
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

@app.get('/api/v1/websites/{website_id}', response_model=WebsiteOut)
def get_website(website_id: int, db: Session = Depends(get_db)):
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail='Website not found')

    latest_crawl = (
        db.query(CrawlResult)
        .filter(CrawlResult.website_id == website.id)
        .order_by(desc(CrawlResult.timestamp))
        .first()
    )

    website.latest_crawl = latest_crawl

    return website

@app.put('/api/v1/websites/{website_id}', response_model=WebsiteOut)
def update_website(website_id: int, updated: WebsiteCreate, db: Session = Depends(get_db)):
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail='Website not found')
    for key, value in updated.dict().items():
        setattr(website, key, str(value) if key == 'url' else value)
    db.commit()
    db.refresh(website)
    return website

@app.delete('/api/v1/websites/{website_id}', status_code=204)
def delete_website(website_id: int, db: Session = Depends(get_db)):
    website = db.query(Website).filter(Website.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail='Website not found')
    db.delete(website)
    db.commit()
    return

@app.get('/api/v1/crawl-results/{website_id}', response_model=List[CrawlResultOut])
def get_crawl_results(website_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(CrawlResult)
        .filter(CrawlResult.website_id == website_id)
        .order_by(CrawlResult.timestamp.desc())
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail="No crawl results found for this website")

    return results

# APScheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(crawl_sites, 'interval', minutes=1)  # Change interval as needed
scheduler.start()

@app.on_event('shutdown')
def shutdown_event():
    scheduler.shutdown()