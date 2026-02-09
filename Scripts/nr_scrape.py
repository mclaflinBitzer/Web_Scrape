# %%
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime


# %%
def nr_fetch_method(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers, verify=False, timeout=30)
    print(response.status_code)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup

# %% [markdown]
# ### Extract links from base NR URL

# %%
def nr_url_extraction(temp_soup):
    # Find the div where class contains 'ecs-posts' & extract all links
    posts_div = temp_soup.find("div", class_=re.compile(r"ecs-posts"))

    if posts_div:
        links = [
            a["href"]
            for a in posts_div.find_all("a", class_=re.compile(r"elementor-button"))
            if a.get("href")
        ]
        print(links)
        deduped_list = list(set(links))
        return deduped_list
    else:
        print("No matching div found")
        return []

# %% [markdown]
# ### Scraping method to extract article data from each articles link previously extracted

# %%
def nr_article_scraping_method(link):
    article_html = nr_fetch_method(link)

    new_data = pd.DataFrame(columns=['title', 'summary', 'dateline', 'newslinetext', 'attachmenturl','source'])

    title = article_html.find("h2", class_=re.compile(r"elementor-heading-title")).get_text()

    container = article_html.find('div', class_='elementor-element elementor-element-0f340ec newslinks elementor-widget elementor-widget-theme-post-content')

    if container:
        temp_wid_cont = container.find_all('div', class_='elementor-widget-container')
        temp_summary = temp_wid_cont[0].get_text().strip()
    else:
        temp_summary = 'no content found'


    split_sum = temp_summary.split('.')
    shortened_sum = '.'.join(split_sum[:3])+'.'

    info_section = article_html.find('div', class_='elementor-container elementor-column-gap-default')
    publication_date = info_section.find('time').get_text().strip()
    dateline = datetime.strptime(publication_date, '%B %d, %Y')

    content_html = article_html.find('div', class_='elementor-element elementor-element-0f340ec newslinks elementor-widget elementor-widget-theme-post-content')
    article_body = content_html.get_text().strip()
    article_body = article_body.split("Atricle previews")[0].strip()

    new_row = {'title':title, 'summary':shortened_sum, 'dateline':dateline, 'newslinetext':article_body, 'attachmenturl':link, 'source':'Natural Refrigerants'}
    new_data = pd.concat([new_data, pd.DataFrame([new_row])], ignore_index=True)
    return new_data
    
 
