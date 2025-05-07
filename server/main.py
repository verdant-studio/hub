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

import base64
import requests
import logging

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
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
    db = SessionLocal()
    sites = db.query(Website).all()

    if not sites:
        print("No websites to crawl.")
        db.close()
        return

    for site in sites:
        try:
            start = datetime.utcnow()
            url = f"{site.url.rstrip('/')}/relay/v1/core"

            # Encode username and app_password as Base64
            credentials = f"{site.username}:{site.app_password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()

            # Add Authorization header
            headers = {
                "Authorization": f"Basic {encoded_credentials}"
            }

            response = requests.get(url, headers=headers, timeout=10, verify=False) # TODO: verify=False is insecure, consider using a proper SSL certificate
            elapsed_ms = int((datetime.utcnow() - start).total_seconds() * 1000)

            print(f"Crawling {response} took {elapsed_ms} ms")

            if response.status_code == 200:
                try:
                    data = response.json()

                    # Only store if essential fields are present
                    if all(k in data for k in ["wp_version", "health_rating", "updates_available"]):
                        result = CrawlResult(
                            website_id=site.id,
                            status_code=response.status_code,
                            response_time_ms=elapsed_ms,
                            wp_version=data["wp_version"],
                            health_rating=data["health_rating"],
                            updates_available=data["updates_available"],
                            timestamp=datetime.utcnow(),
                        )
                        db.add(result)
                        db.commit()
                        prune_old_crawls(db, site.id, keep=5)
                    else:
                        print(f"Incomplete data from {url}, skipping.")

                except ValueError:
                    print(f"Invalid JSON from {url}, skipping.")

            else:
                print(f"Non-200 response from {url}, skipping.")

        except Exception as e:
            print(f"Error crawling {url}: {e}")

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