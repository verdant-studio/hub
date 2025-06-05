import base64
import requests
from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Website, CrawlResult
from settings import fernet

# Configuration toggle
VERIFY_SSL = True  # Set to False only for debugging

def prune_old_crawls(db: Session, website_id: int, keep: int = 5):
    """Delete old crawl results, keeping only the most recent `keep`."""
    subquery = (
        select(CrawlResult.id)
        .where(CrawlResult.website_id == website_id)
        .order_by(CrawlResult.timestamp.desc())
        .offset(keep)
    ).subquery()

    db.execute(delete(CrawlResult).where(CrawlResult.id.in_(select(subquery.c.id))))
    db.commit()

def build_auth_headers(site: Website) -> dict:
    """Return Basic Auth headers for a given site."""
    decrypted_pw = fernet.decrypt(site.app_password.encode()).decode()
    credentials = f"{site.username}:{decrypted_pw}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}

def fetch_site_data(url: str, headers: dict) -> tuple:
    """Send GET request and return response + elapsed time in ms."""
    start = datetime.utcnow()
    response = requests.get(url, headers=headers, timeout=10, verify=VERIFY_SSL)
    elapsed_ms = int((datetime.utcnow() - start).total_seconds() * 1000)
    return response, elapsed_ms

def handle_crawl_response(db: Session, site: Website, response, elapsed_ms: int):
    """Handle the response and store the crawl result in the database."""
    result = CrawlResult(
        website_id=site.id,
        status_code=response.status_code,
        response_time_ms=elapsed_ms,
        wp_version=None,
        health_rating=None,
        updates_available=None,
        timestamp=datetime.utcnow(),
        multisite=None,
        subsites=None,
    )

    if response.status_code == 200:
        try:
            data = response.json()
            required_keys = ['wp_version', 'health_rating', 'updates_available', 'multisite', 'subsites']

            if all(key in data for key in required_keys):
                result.wp_version = data['wp_version']
                result.health_rating = data['health_rating']
                result.updates_available = data['updates_available']
                result.multisite = data['multisite']
                result.subsites = data['subsites'] if data['multisite'] else None
            else:
                print(f"[{site.url}] Missing fields in response; skipping details.")
        except ValueError:
            print(f"[{site.url}] Invalid JSON; skipping details.")
    else:
        print(f"[{site.url}] Non-200 response: {response.status_code}")

    db.add(result)
    db.commit()

def crawl_single_site(db: Session, site: Website):
    """Crawl a single website and store the result."""
    try:
        url = f"{site.url.rstrip('/')}/wp-json/relay/v1/core"
        headers = build_auth_headers(site)
        response, elapsed_ms = fetch_site_data(url, headers)
        handle_crawl_response(db, site, response, elapsed_ms)
    except requests.RequestException as e:
        print(f"[{site.url}] Network error: {e}")
    except Exception as e:
        print(f"[{site.url}] Unexpected error: {e}")

def crawl_sites():
    """Crawl all websites stored in the database."""
    with SessionLocal() as db:
        sites = db.query(Website).all()

        if not sites:
            print("No websites to crawl.")
            return

        for site in sites:
            crawl_single_site(db, site)
            prune_old_crawls(db, site.id, keep=5)
