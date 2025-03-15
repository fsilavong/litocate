import unittest

from litocate.data.base import Paper
from litocate.data.pubmed import PubMedArticle

class BaseTestCase(unittest.TestCase):
    def test_paper_from_pubmed(self):
        obj_key = 'tests/data/PMC10034384.xml'
        xml_str = open(obj_key).read()
        article = PubMedArticle.from_string(xml_str)
        paper = Paper.from_pubmed_article(article)
        self.assertDictEqual(
            paper.as_json(),
            {
                'title': 'Corrigendum: Effect of Allium sativum and Nigella\n                    sativa on alleviating aluminum toxicity state in the albino rats', 
                'abstract': None, 
                'is_peer_reviewed': True, 
                'metadata': {
                    'doi': '10.3389/fvets.2023.1160163', 
                    'pmid': None, 
                    'pmc': 'PMC10034384', 
                    'pub_year': '2023', 
                    'url': "https://pmc.ncbi.nlm.nih.gov/articles/PMC10034384/",
                    'journal': 'Frontiers in Veterinary Science'
                }
            }
        )