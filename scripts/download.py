import os
import json 
import datetime

from litocate.data.pubmed import PubMedClient
from litocate.data.acl import AnthologyClient
from litocate.data.constant import DS_FORMAT, LAST_UPDATE_KEY, RESULT_KEY, PUBMED_FOLDERS

max_threads = min(32, (os.cpu_count() or 1) * 2)
download_datetime = datetime.datetime.now().strftime(DS_FORMAT)
keywords = ['text simplification', 'sentence simplification', 'text style transfer',
    'text adaptation', 'lexical simplification', 'readability']
pub_after_year = 2021

results = []

for pubmed_folder in PUBMED_FOLDERS:
    pubmed_result = PubMedClient(
        folder=pubmed_folder    
    ).find_papers(
        keywords=keywords,
        pub_after_year=pub_after_year,
        max_threads=max_threads,
    )
    results.extend(pubmed_result)
    
acl_result = AnthologyClient().find_papers(
    keywords=keywords, 
    pub_after_year=pub_after_year
)
results.extend(acl_result)

with open(f'result.json', 'w') as f:
    json.dump({
        RESULT_KEY: results,
        LAST_UPDATE_KEY: download_datetime
    }, f, indent=4)
