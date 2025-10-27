import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta, timezone

class GlassdoorScraper:
    def __init__(self):
        self.base_url = "https://www.glassdoor.com"
    
    async def fetch_jobs(self, keywords: str = "software engineer", location: str = "Remote", limit: int = 20) -> List[Dict]:
        """Scrape Glassdoor jobs"""
        jobs = []
        
        try:
            async with aiohttp.ClientSession() as session:
                search_url = f"{self.base_url}/Job/jobs.htm?sc.keyword={keywords.replace(' ', '+')}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(search_url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Parse job listings
                        job_listings = soup.find_all('li', class_='react-job-listing', limit=limit)
                        
                        for listing in job_listings:
                            try:
                                title_elem = listing.find('a', class_='jobLink')
                                company_elem = listing.find('div', class_='employerName')
                                location_elem = listing.find('span', class_='loc')
                                
                                if title_elem and company_elem:
                                    jobs.append({
                                        'job_id': f"glassdoor_{len(jobs)+1}",
                                        'source': 'glassdoor',
                                        'title': title_elem.text.strip(),
                                        'company': company_elem.text.strip(),
                                        'description': 'View job details on Glassdoor',
                                        'location': location_elem.text.strip() if location_elem else location,
                                        'url': f"{self.base_url}{title_elem['href']}" if 'href' in title_elem.attrs else search_url,
                                        'posted_date': datetime.now(timezone.utc) - timedelta(hours=15)
                                    })
                            except Exception:
                                continue
        except Exception as e:
            print(f"Glassdoor scraping error: {e}")
        
        return jobs