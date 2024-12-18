import datetime
import json

from litocate.data.constant import PUBMED_FOLDERS
from litocate.data.utils import compound_token_match
from litocate.data.constant import DS_FORMAT, LAST_UPDATE_KEY, RESULT_KEY
from litocate.llm.filter import LLMClassifier

results = []
for folder in PUBMED_FOLDERS:
    results.extend(json.load(open(f'../result_from_{folder}.json')))
    
compound_keywords = [
   ['text simplification', 'sentence simplification', 'text style transfer',
    'text adaptation', 'lexical simplification', 'readability'],
   ['biomedical', 'medical', 'clinical', 'healthcare'], 
]
execute_datetime = datetime.datetime.now().strftime(DS_FORMAT)

count = 0
filtered_results = []
for r in results:
    matches = []
    matches.append(compound_token_match(
        r['title'], compound_keywords
    ))
    if r['abstract']:
        for content in r['abstract'].values():
            matches.append(compound_token_match(
                content, compound_keywords
            ))
    if any(matches):
        filtered_results.append(r)

classifier = LLMClassifier()
for r in filtered_results:
    passage = f"""
    {r['title']}
    
    {" ".join(r['abstract'].values()) if r['abstract'] else ""}
    """
    classification = classifier.classify(passage)
    r['is_relevant_pred'] = classification.relevant
    r['is_relevant_truth'] = classification.relevant # Human Evaluation Placeholder

with open('filtered_result.json', 'w') as outf:
    json.dump({
        RESULT_KEY: filtered_results,
        LAST_UPDATE_KEY: execute_datetime
    }, outf, indent=4)
