
from database import SessionLocal
from models import Website
from sqlalchemy.orm import Session
import aiohttp

async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return url, response.status
    except Exception as e:
        return url, str(e)

async def crawl_sites():
    db: Session = SessionLocal()
    sites = db.query(Website).all()
    db.close()

    urls = [site.url for site in sites]

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(fetch_url(session, url) for url in urls))
        for url, result in results:
            print(f"[CRAWL] {url} → {result}")