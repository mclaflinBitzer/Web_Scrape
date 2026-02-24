# %%
import pandas as pd
from dotenv import load_dotenv
import os
import requests
import logging
from Scripts.logger import setup_logger

# %% [markdown]
# ### API Push 

# %%
def api_push(logger):
    load_dotenv()

    logger.info("Fetching api credentials and keys from .env file")
    api_url = os.getenv("api_url")
    APIid = os.getenv("APIid")
    authKey =  os.getenv("authKey")
    customerGUID = os.getenv("customerGUID")
    accessGroups = os.getenv("accessGroups")

    logger.info("Reading compiled article data from excel file")
    df = pd.read_excel(os.getenv("output_file"))

    for index, row in df.iterrows():
        data = {
                "APIid": APIid, 
                "customerGUID": customerGUID, 
                "authKey": authKey,
                "title": str(row['title']), 
                "summary": str(row['summary']),
                "body": str(row['newslinetext']),
                "source": str(row['source']), 
                "pubdate": row['dateline'].isoformat(),
                "link": row['attachmenturl'], 
                "topicIds": 135575, 
                "accessGroup": accessGroups 

        }

        r = requests.post(api_url, data=data, verify=False)
        logger.info(f"API response status code for article '{row['title']}': {r.status_code} and the content {r.content}")
        if r.status_code != 200:
            logger.error(f"Failed to push article '{row['title']}' to API. Status code: {r.status_code}, Response: {r.content}")
        #print(r)
        #print(r.content)


