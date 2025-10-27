import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta, timezone

class StartupsGalleryScraper:
    def __init__(self):
        self.base_url = "https://startups.gallery"
    
    async def fetch_jobs(self, keywords: str = "software engineer", limit: int = 20) -> List[Dict]:
        """Scrape Startups.gallery jobs"""
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
                        
                        # Parse job listings
                        job_listings = soup.find_all('div', class_='job-listing', limit=limit)
                        
                        for listing in job_listings:
                            try:
                                title_elem = listing.find('h3')
                                company_elem = listing.find('div', class_='company-name')
                                link_elem = listing.find('a')
                                
                                if title_elem and company_elem:
                                    jobs.append({
                                        'job_id': f"startups_gallery_{len(jobs)+1}",
                                        'source': 'startups_gallery',
                                        'title': title_elem.text.strip(),
                                        'company': company_elem.text.strip(),
                                        'description': 'Startup job opportunity',
                                        'location': 'Remote/Flexible',
                                        'url': link_elem['href'] if link_elem and 'href' in link_elem.attrs else search_url,
                                        'posted_date': datetime.now(timezone.utc) - timedelta(hours=10)
                                    })
                            except Exception:
                                continue
        except Exception as e:
            print(f"Startups.gallery scraping error: {e}")
        
        return jobs