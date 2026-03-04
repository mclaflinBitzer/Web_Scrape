
# 📰 News Scraper & API Integration

## 📌 Overview

This project scrapes news articles from:

* **Natural Refrigerants** – [https://naturalrefrigerants.com/news/](https://naturalrefrigerants.com/news/)
* **Trane Technologies** – [https://www.tranetechnologies.com/en/index/news.html](https://www.tranetechnologies.com/en/index/news.html)

The pipeline:

1. Scrapes article links from each website
2. Extracts article content (title, summary, body, publication date)
3. Compiles all articles into a single DataFrame
4. Exports the results to Excel
5. Pushes the compiled data to the **Comintelli API**

---

# 🏗 Project Structure

```
Project Root
│
├── Scripts/
│   ├── nr_scrape.py
│   ├── trane_scrape.py
│   └── API_push.py
│
├── Data/
│   └── compiled_article_data.xlsx
│
├── main.ipynb
└── README.md
```

---

# ⚙️ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔄 Full Workflow

## 1️⃣ Base URLs

```python
nr_url = 'https://naturalrefrigerants.com/news/'
trane_url = 'https://www.tranetechnologies.com/en/index/news.html'
```

---

## 2️⃣ Data Structure

All scraped articles are compiled into a single DataFrame with the following schema:

| Column Name   | Description                  |
| ------------- | ---------------------------- |
| title         | Article title                |
| summary       | First 3 sentences of article |
| dateline      | Publication date (datetime)  |
| newslinetext  | Full article body            |
| attachmenturl | Original article URL         |
| source        | News source name             |

---

# 🧊 Natural Refrigerants Scraper

### Step 1: Fetch Base Page

`nr_fetch_method(url)`

* Sends HTTP GET request with browser headers
* Returns parsed BeautifulSoup object

### Step 2: Extract Article Links

`nr_url_extraction(soup)`

* Locates div containing `ecs-posts`
* Extracts article URLs
* Removes duplicates
* Returns list of links

### Step 3: Scrape Individual Articles

`nr_article_scraping_method(link)`

Extracts:

* Title
* Summary (first 3 sentences)
* Publication date
* Full article body
* Source name

Returns a DataFrame containing one row per article.

---

# 🌬 Trane Technologies Scraper

### Step 1: Fetch Base Page

`trane_fetch_method(url)`

* Uses same request logic as NR scraper

### Step 2: Extract Article Links

`trane_url_extraction(soup)`

* Finds `<a>` tags with class `newspromo__link`
* Filters for HTTPS links
* Returns article URLs

### Step 3: Scrape Individual Articles

`trane_scrape_article(url)`

Extracts:

* Title
* Full article text
* Summary (first 3 sentences)
* Publication date (with multiple parsing fallbacks)
* Source name

If no date is found:

* Defaults to `datetime.now()`

---

# 📊 Data Compilation

Both scrapers append results into:

```python
compiled_article_data = pd.DataFrame(
    columns=['title', 'summary', 'dateline', 'newslinetext', 'attachmenturl','source']
)
```

All scraped articles are concatenated into this master DataFrame.

---

# 📁 Export to Excel

After scraping:

```python
compiled_article_data.to_excel(
    'Data/compiled_article_data.xlsx',
    index=False
)
```

This creates:

```
Data/compiled_article_data.xlsx
```

---

# 🚀 API Integration

## Environment Variables

The API push requires a `.env` file in the project root:

```
api_url=YOUR_API_ENDPOINT
APIid=YOUR_API_ID
authKey=YOUR_AUTH_KEY
customerGUID=YOUR_CUSTOMER_GUID
accessGroups=YOUR_ACCESS_GROUP
```

These are loaded using:

```python
from dotenv import load_dotenv
```

---

## API Push Process

`api_push()`

1. Reads compiled Excel file
2. Iterates through each article
3. Sends POST request to API

Payload fields:

```json
{
  "APIid": "...",
  "customerGUID": "...",
  "authKey": "...",
  "title": "...",
  "summary": "...",
  "body": "...",
  "source": "...",
  "pubdate": "...",
  "link": "...",
  "topicIds": 135575,
  "accessGroup": "..."
}
```

Each article is pushed individually.

---

# ▶️ How to Run

1. Ensure `.env` file is configured
2. Run all cells within the main.ipynb file:


Pipeline execution order:

1. Scrape Natural Refrigerants
2. Scrape Trane Technologies
3. Compile results
4. Save Excel file
5. Push to API

---
