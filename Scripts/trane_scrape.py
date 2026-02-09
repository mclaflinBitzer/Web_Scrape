# %%
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime

# %%
trane_url = 'https://www.tranetechnologies.com/en/index/news.html'
## works w/ base fetch

##trane_news_url = 'https://investors.tranetechnologies.com/news-and-events/news-releases/default.aspx'
## doesn't work w/ base fetch

trane_article_url = 'https://investors.tranetechnologies.com/news-and-events/news-releases/news-release-details/2025/Trane-Technologies-to-Acquire-Stellar-Energy-Digital-Business/default.aspx'
## works w/ base fetch


# %% [markdown]
# ### original base fetch method

# %%
def trane_fetch_method(url):
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
# ### Extract htmls

# %%
def trane_url_extraction(temp_soup):
    # Find all <a> tags with class newspromo__link
    links = temp_soup.find_all("a", class_="newspromo__link")

    # Extract href attributes
    hrefs = [a['href'] for a in links if 'href' in a.attrs]

    # Keep only links that start with https:
    https_links = [link for link in hrefs if link.startswith("https:")]
    return https_links

# %% [markdown]
# ### Trane article scraping method

# %%
def trane_scrape_article(url):
    print(url)
    soup = trane_fetch_method(url)

    new_data = pd.DataFrame(columns=['title','summary','dateline','newslinetext','url','source'])

    ## extract title
    title=soup.find('h3').get_text().strip()


    ## extract summary / newslinetext 
    full_text = " ".join(p.get_text().strip() for p in soup.find_all('p'))
    result_text = full_text.split("About Trane Technologies")[0].strip()
    result_text = result_text.split("About Trane")[0].strip()

    ## extract date
    dateline = None

    try:
        date_text=soup.find("span", class_="module_date-text").get_text().strip()
        dateline = datetime.strptime(date_text, '%b %d, %Y')
    except Exception:
        ## fallback to span value
        spans = soup.find_all("span", class_="value")

        for span in spans:
            text = span.get_text(strip=True)  # extract text from each span

            try:
                dateline = datetime.strptime(text, '%b %d, %Y')
                break  # exit loop if date is found
            except ValueError:
                pass
            try:
                text_clean = text.replace(" ET", "")  # remove timezone suffix
                dateline = datetime.strptime(text_clean, "%b %d, %Y %I:%M %p")
                break
            except ValueError:
                pass
    if dateline is None:
        dateline = datetime.now()

    split_text = result_text.split('.')
    summary = '.'.join(split_text[:3]) + '.'

    new_row = {'title':title, 'summary':summary, 'dateline':dateline, 'newslinetext':result_text, 'url':url, 'source':'Trane Technologies'}
    new_data = pd.concat([new_data, pd.DataFrame([new_row])], ignore_index=True)
    return new_data



# %% [markdown]
# # Implementation

# %%
## scrape homepage url for article links
temp_soup = trane_fetch_method(trane_url)

# # Find all <a> tags with class newspromo__link
# links = temp_soup.find_all("a", class_="newspromo__link")

# # Extract href attributes
# hrefs = [a['href'] for a in links if 'href' in a.attrs]

# # Keep only links that start with https:
# https_links = [link for link in hrefs if link.startswith("https:")]


https_links = trane_url_extraction(temp_soup)

## iterate through article links and scrape each articles data

article_data = pd.DataFrame(columns=['title','summary','dateline','newslinetext','url', 'source'])

for link in https_links:
    article_data = pd.concat([article_data, trane_scrape_article(link)], ignore_index=True)

# %%
## write to excel
article_data.to_excel('trane_news.xlsx', index=False)


