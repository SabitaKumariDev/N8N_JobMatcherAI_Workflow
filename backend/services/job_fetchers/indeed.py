import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta, timezone

class IndeedScraper:
    def __init__(self):
        self.base_url = "https://www.indeed.com"
    
    async def fetch_jobs(self, keywords: str = "software engineer", location: str = "Remote", limit: int = 20) -> List[Dict]:
        """Scrape Indeed jobs (last 24 hours)"""
        jobs = []
        
        try:
            async with aiohttp.ClientSession() as session:
                search_url = f"{self.base_url}/jobs?q={keywords.replace(' ', '+')}&l={location}&fromage=1"  # fromage=1 = last day
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(search_url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Parse job cards
                        job_cards = soup.find_all('div', class_='job_seen_beacon', limit=limit)
                        
                        for card in job_cards:
                            try:
                                title_elem = card.find('h2', class_='jobTitle')
                                company_elem = card.find('span', class_='companyName')
                                location_elem = card.find('div', class_='companyLocation')
                                snippet_elem = card.find('div', class_='job-snippet')
                                link_elem = card.find('a', class_='jcs-JobTitle')
                                
                                if title_elem and company_elem:
                                    job_url = f"{self.base_url}{link_elem['href']}" if link_elem and 'href' in link_elem.attrs else search_url
                                    
                                    jobs.append({
                                        'job_id': f"indeed_{len(jobs)+1}",
                                        'source': 'indeed',
                                        'title': title_elem.text.strip(),
                                        'company': company_elem.text.strip(),
                                        'description': snippet_elem.text.strip() if snippet_elem else 'View job details on Indeed',
                                        'location': location_elem.text.strip() if location_elem else location,
                                        'url': job_url,
                                        'posted_date': datetime.now(timezone.utc) - timedelta(hours=8)
                                    })
                            except Exception:
                                continue
        except Exception as e:
            print(f"Indeed scraping error: {e}")
        
        return jobs