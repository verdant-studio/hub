async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return url, response.status
    except Exception as e:
        return url, str(e)