import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta, timezone

class WellfoundScraper:
    def __init__(self):
        self.base_url = "https://wellfound.com"
    
    async def fetch_jobs(self, keywords: str = "software engineer", limit: int = 20) -> List[Dict]:
        """Scrape Wellfound (formerly AngelList) jobs"""
        jobs = []
        
        try:
            async with aiohttp.ClientSession() as session:
                search_url = f"{self.base_url}/jobs"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(search_url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Parse Wellfound job cards
                        job_cards = soup.find_all('div', {'data-test': 'JobSearchResult'}, limit=limit)
                        
                        for card in job_cards:
                            try:
                                title_elem = card.find('h2')
                                company_elem = card.find('h3')
                                link_elem = card.find('a')
                                
                                if title_elem and company_elem:
                                    jobs.append({
                                        'job_id': f"wellfound_{len(jobs)+1}",
                                        'source': 'wellfound',
                                        'title': title_elem.text.strip(),
                                        'company': company_elem.text.strip(),
                                        'description': 'Startup job on Wellfound',
                                        'location': 'Remote/Flexible',
                                        'url': f"{self.base_url}{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else search_url,
                                        'posted_date': datetime.now(timezone.utc) - timedelta(hours=7)
                                    })
                            except Exception:
                                continue
        except Exception as e:
            print(f"Wellfound scraping error: {e}")
        
        return jobs