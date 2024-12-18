import unittest

from litocate.data.pubmed import PubMedClient, PubMedArticle

class PubMedArticleTestCase(unittest.TestCase):
    def test_from_string_valid(self):
        xml_str = open('tests/data/PMC9671157.xml').read()
        abstract = {
            'title_content_0': 'Automated simplification models aim to make input texts more readable. Such methods have the potential to make complex information accessible to a wider audience, e.g., providing access to recent medical literature which might otherwise be impenetrable for a lay reader. However, such models risk introducing errors into automatically simplified texts, for instance by inserting statements unsupported by the corresponding original text, or by omitting key information. Providing more readable but inaccurate versions of texts may in many cases be worse than providing no such access at all. The problem of factual accuracy (and the lack thereof) has received heightened attention in the context of summarization models, but the factuality of automatically simplified texts has not been investigated. We introduce a taxonomy of errors that we use to analyze both references drawn from standard simplification datasets and state-of-the-art model outputs. We find that errors often appear in both that are not captured by existing evaluation metrics, motivating a need for research into ensuring the factual accuracy of automated simplification models.'
        }
        article = PubMedArticle.from_string(xml_str)
        self.assertEqual(
            article.abstract, abstract
        )
        self.assertEqual(
            article.title, 'Evaluating Factuality in Text Simplification'
        )
        self.assertEqual(
            article.doi, '10.18653/v1/2022.acl-long.506'
        )
        self.assertEqual(
            int(article.pub_year), 2022
        )
        self.assertEqual(
            article.peer_reviewed, True
        )
    
    def test_from_string_valid_2(self):
        xml_str = open('tests/data/PMC10034384.xml').read()
        article = PubMedArticle.from_string(xml_str)
        self.assertIsNone(article.abstract)
        clean_title = " ".join([
            token for token in article.title.replace('\n', '').split(' ')
            if token
        ])
        self.assertEqual(
            clean_title, 'Corrigendum: Effect of Allium sativum and Nigella sativa on alleviating aluminum toxicity state in the albino rats'
        )
        self.assertEqual(
            article.doi, '10.3389/fvets.2023.1160163'
        )
        self.assertEqual(
            int(article.pub_year), 2023
        )
        self.assertEqual(
            article.peer_reviewed, True
        )
    
    def test_from_string_invalid(self):
        article = PubMedArticle.from_string('')
        for attr in ['abstract', 'title', 'doi', 'pub_year', 'peer_reviewed']:
            self.assertIsNone(getattr(article, attr))

if __name__=='__main__':
    unittest.main()