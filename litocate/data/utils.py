from typing import List 
import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.stem.porter import PorterStemmer

def keyword_exist(string, keywords, lower=True):
    if lower:
        string = string.lower()
        keywords = [k.lower() for k in keywords]
    for keyword in keywords:
        if keyword in string:
            return True
    return False

def compound_token_match(
    string: str,
    keywords_list: List[List[str]]
):
    stemmer = PorterStemmer()
    string = string.lower()
    tokens = [stemmer.stem(t) for t in word_tokenize(string)]
    and_condition = []
    for keyword in keywords_list:
        or_condition = []
        for kw in keyword:
            stem_kw = [stemmer.stem(t).lower() for t in word_tokenize(kw)]
            n = len(stem_kw)
            or_condition.extend(
                [ngram_kw in ngrams(tokens, n) for ngram_kw in ngrams(stem_kw, n)]
            )
        and_condition.append(any(or_condition))
    return all(and_condition)

def compound_keyword_match(
    string: str,
    keywords_list: List[List[str]]
):
    and_condition = []
    for keywords in keywords_list:
        and_condition.append(any(
            [k.lower() in string.lower() for k in keywords]
        ))
    return all(and_condition)
