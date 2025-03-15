from dataclasses import dataclass

@dataclass
class Paper:
    title: str
    abstract: dict
    is_peer_reviewed: bool
    metadata: dict
    
    def from_pubmed_article(article):
        if article.pmid:
            url = f"https://pubmed.ncbi.nlm.nih.gov/{article.pmid}/"
        elif article.pmc:
            url = f"https://pmc.ncbi.nlm.nih.gov/articles/{article.pmc}/"
        else:
            url = None
        
        return Paper(
            title=article.title,
            abstract=article.abstract,
            is_peer_reviewed=article.peer_reviewed,
            metadata={
                'doi': article.doi,
                'pmid': article.pmid,
                'pmc': article.pmc,
                'pub_year': article.pub_year,
                'url': url,
                'journal': article.journal
            }
        )
    
    def from_acl_paper(acl_paper):
        return Paper(
            title= acl_paper.title.as_text(),
            abstract = {
                'abstract': acl_paper.abstract.as_text() if acl_paper.abstract else None
            },
            is_peer_reviewed = True,
            metadata= {
                'bibtext': acl_paper.to_bibtex(),
                'anthology_id': acl_paper.full_id,
                'pub_year': acl_paper.year,
                'url': f'https://aclanthology.org/{acl_paper.full_id}' if acl_paper.full_id else None
        })
        
    def as_json(self):
        return {
            'title': self.title,
            'abstract': self.abstract,
            'is_peer_reviewed': self.is_peer_reviewed,
            'metadata': self.metadata
        }

    def __getitem__(self, key):
        return getattr(self, key)