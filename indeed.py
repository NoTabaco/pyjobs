import requests
from bs4 import BeautifulSoup

LIMIT = 50
BASE_URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page(url = BASE_URL, last_page = 0):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination_list = soup.find("ul", {"class": "pagination-list"})
    links = pagination_list.find_all("a")
    pages = []

    if(len(links) == 5 or len(links) == 6):
        for link in links:
            if link.string is None: continue
            pages.append(int(link.string))
        last_page = pages[-1]
        return get_last_page(f"{BASE_URL}&start={last_page * 50}", last_page)
    elif last_page > 5 and len(links) < 5:
        for link in links:
            if link.string is None: continue
            pages.append(int(link.string))
        return last_page
    else:
        return len(links)

def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    if company:
        company_anchor = company.find("a")
        if(company_anchor is not None):
            company = str(company_anchor.string)
        else:
            company = str(company.string)
        company = company.strip()
    else:
        company = None
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        "title": title, 
        "company": company, 
        "location": location, 
        "link": f"https://www.indeed.com/viewjob?jk={job_id}"
        }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page #{page + 1}")
        result = requests.get(f"{BASE_URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs