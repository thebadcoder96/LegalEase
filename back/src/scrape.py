import aiohttp

from bs4 import BeautifulSoup


default_header = {
    "User-Agent": "LegalEaseUserAgent",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            headers=default_header,
            ssl=None,
        ) as response:
            if response.status != 200:
                raise Exception(f'Failed to fetch {url}: {response.status}')
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
    # TODO: Save the document to a database
    return doc
