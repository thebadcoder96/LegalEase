import aiohttp

from bs4 import BeautifulSoup

async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return f'Failed to fetch {url}: {response.status}'
            return await response.text()
        
async def scrape(url: str) -> str:
    doc = {'source': url}
    html = await fetch(url)
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("title"):
        doc['title'] = soup.find("title").get_text()
    if soup.find("meta", attrs={"name": "description"}):
        doc['description'] = soup.find("meta", attrs={"name": "description"}).get("content", "N/A")
    if soup.find("html"):
        doc['language'] = soup.find("html").get("lang", "N/A")
    doc['content'] = soup.get_text()
    return doc
