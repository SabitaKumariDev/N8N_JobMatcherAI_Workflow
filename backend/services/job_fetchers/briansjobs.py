import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta, timezone

class BriansJobsScraper:
    def __init__(self):
        self.base_url = "https://briansjobsearch.com"
    
    async def fetch_jobs(self, keywords: str = "software engineer", limit: int = 20) -> List[Dict]:
        """Scrape Brian's Job Search"""
        jobs = []
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(self.base_url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Parse job cards
                        job_cards = soup.find_all('div', class_='job-card', limit=limit)
                        
                        for card in job_cards:
                            try:
                                title_elem = card.find('h2')
                                company_elem = card.find('p', class_='company')
                                link_elem = card.find('a')
                                
                                if title_elem:
                                    jobs.append({
                                        'job_id': f"briansjobs_{len(jobs)+1}",
                                        'source': 'briansjobs',
                                        'title': title_elem.text.strip(),
                                        'company': company_elem.text.strip() if company_elem else 'Various Companies',
                                        'description': 'Tech job opportunity',
                                        'location': 'Remote',
                                        'url': link_elem['href'] if link_elem and 'href' in link_elem.attrs else self.base_url,
                                        'posted_date': datetime.now(timezone.utc) - timedelta(hours=6)
                                    })
                            except Exception:
                                continue
        except Exception as e:
            print(f"Brian's Jobs scraping error: {e}")
        
        return jobs