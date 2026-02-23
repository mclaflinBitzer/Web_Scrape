# %%
import pandas as pd
from dotenv import load_dotenv
import os
import requests

# %% [markdown]
# ### API Push 

# %%
def api_push():
    load_dotenv()

    api_url = os.getenv("api_url")
    APIid = os.getenv("APIid")
    authKey =  os.getenv("authKey")
    customerGUID = os.getenv("customerGUID")
    accessGroups = os.getenv("accessGroups")

    df = pd.read_excel('Data/compiled_article_data.xlsx')

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
        print(r)
        print(r.content)


