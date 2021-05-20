import requests
from bs4 import BeautifulSoup

indeed_base_url = "https://www.indeed.com/jobs?q=python&limit=50"

def get_pages(url, last_page):
    indeed_result = requests.get(url)
    indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')

    pagination_list = indeed_soup.find("ul", {"class": "pagination-list"})
    links = pagination_list.find_all("a")
    pages = []

    if(len(links) == 5 or len(links) == 6):
        for link in links:
            if link.string is None: continue
            pages.append(int(link.string))
        last_page = pages[-1]
        return get_pages(f"https://www.indeed.com/jobs?q=python&limit=50&start={(last_page - 1) * 50}", last_page)
    elif last_page > 5 and len(links) < 5:
        for link in links:
            if link.string is None: continue
            pages.append(int(link.string))
        return last_page
    else:
        return len(links)
    
total_page = get_pages(indeed_base_url, 1)

print(total_page)