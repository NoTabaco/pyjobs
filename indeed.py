import requests
from bs4 import BeautifulSoup

LIMIT = 50
BASE_URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages(url = BASE_URL, last_page = 0):
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
        return extract_indeed_pages(f"{BASE_URL}&start={last_page * 50}", last_page)
    elif last_page > 5 and len(links) < 5:
        for link in links:
            if link.string is None: continue
            pages.append(int(link.string))
        return last_page
    else:
        return len(links)

def extract_indeed_jobs(last_page):
    jobs = []
    #for page in range(last_page):
    result = requests.get(f"{BASE_URL}&start={0*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        title = result.find("h2", {"class": "title"}).find("a")["title"]
        print(title)
    return jobs