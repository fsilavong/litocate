import logging

from acl_anthology import Anthology

from litocate.data.base import Paper
from litocate.data.utils import keyword_exist

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()

class AnthologyClient:
    def __init__(self):
        self.client = Anthology.from_repo()
    
    @staticmethod
    def _meet_criteria(text, pub_year, keywords, pub_after_year):
        has_keyword = keyword_exist(text, keywords)
        pub_after   = True if pub_year and int(pub_year) >= pub_after_year else False
        return (has_keyword and pub_after)

    def find_papers(self, keywords, pub_after_year=2021, n=None):
        papers_found = []
        for idx, acl_paper in enumerate(self.client.papers()):
            title = acl_paper.title
            title_match, abstract_match = False, False
            if title:
                title_match =self._meet_criteria(
                    title.as_text(), acl_paper.year, keywords, pub_after_year
                )
            abstract = acl_paper.abstract
            if abstract:
                abstract_match =self._meet_criteria(
                    abstract.as_text(), acl_paper.year, keywords, pub_after_year
                )
            
            if title_match or abstract_match:
                papers_found.append(Paper.from_acl_paper(acl_paper))
            if n and idx >= n:
                break

        return papers_found

    def find_papers_updated_after(self, datetime_str, keywords, pub_after_year):
        return 