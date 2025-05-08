from database import SessionLocal
from datetime import datetime
from models import Website, CrawlResult
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

import base64
import requests

# This function deletes old crawl results, keeping only the most recent `keep` entries
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

# This function crawls a single site and stores the result in the database
def crawl_single_site(db: Session, site: Website):
    try:
        start = datetime.utcnow()
        url = f'{site.url.rstrip("/")}/relay/v1/core'
        response = requests.get(url, timeout=10)

        # Encode username and app_password as Base64
        credentials = f'{site.username}:{site.app_password}'
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        # Add Authorization header
        headers = {
            'Authorization': f'Basic {encoded_credentials}'
        }

        response = requests.get(url, headers=headers, timeout=10, verify=False) # TODO: verify=False is insecure, consider using a proper SSL certificate
        elapsed_ms = int(response.elapsed.total_seconds() * 1000)

        if response.status_code == 200:
            data = response.json()
            if all(k in data for k in ['wp_version', 'health_rating', 'updates_available']):
                result = CrawlResult(
                    website_id=site.id,
                    status_code=response.status_code,
                    response_time_ms=elapsed_ms,
                    wp_version=data['wp_version'],
                    health_rating=data['health_rating'],
                    updates_available=data['updates_available'],
                    timestamp=datetime.utcnow(),
                )
                db.add(result)
                db.commit()
            else:
                print(f'Incomplete crawl data from {url}, skipping.')
        else:
            print(f'Non-200 response from {url}, skipping.')
    except Exception as e:
        print(f'Error crawling {site.url}: {e}')

# This function crawls all sites in the database and stores the results
def crawl_sites():
    db = SessionLocal()
    sites = db.query(Website).all()

    if not sites:
        print('No websites to crawl.')
        db.close()
        return

    for site in sites:
        try:
            start = datetime.utcnow()
            url = f'{site.url.rstrip('/')}/relay/v1/core'

            # Encode username and app_password as Base64
            credentials = f'{site.username}:{site.app_password}'
            encoded_credentials = base64.b64encode(credentials.encode()).decode()

            # Add Authorization header
            headers = {
                'Authorization': f'Basic {encoded_credentials}'
            }

            response = requests.get(url, headers=headers, timeout=10, verify=False) # TODO: verify=False is insecure, consider using a proper SSL certificate
            elapsed_ms = int((datetime.utcnow() - start).total_seconds() * 1000)

            result = CrawlResult(
                website_id=site.id,
                status_code=response.status_code,
                response_time_ms=elapsed_ms,
                wp_version=None,
                health_rating=None,
                updates_available=None,
                timestamp=datetime.utcnow(),
            )
            db.add(result)
            db.commit()

            if response.status_code == 200:
                try:
                    data = response.json()

                    # Only store if essential fields are present
                    if all(k in data for k in ['wp_version', 'health_rating', 'updates_available']):
                        result.wp_version=data['wp_version']
                        result.health_rating=data['health_rating']
                        result.updates_available=data['updates_available']
                        db.commit()
                    else:
                        print(f'Incomplete data from {url}, skipping.')

                except ValueError:
                    print(f'Invalid JSON from {url}, skipping.')

            else:
                print(f'Non-200 response from {url}, skipping.')

        except Exception as e:
            print(f'Error crawling {url}: {e}')

            # Store the error response in the database
            result = CrawlResult(
                website_id=site.id,
                status_code=None, 
                response_time_ms=None,
                wp_version=None,
                health_rating=None,
                updates_available=None,
                timestamp=datetime.utcnow(),
            )

        prune_old_crawls(db, site.id, keep=5)
    db.close()