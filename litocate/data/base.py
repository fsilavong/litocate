from dataclasses import dataclass

@dataclass
class Paper:
    title: str
    abstract: dict
    is_peer_reviewed: bool
    metadata: dict
    
    def from_pubmed_article(article):
        return Paper(
            title=article.title,
            abstract=article.abstract,
            is_peer_reviewed=article.peer_reviewed,
            metadata={
                'doi': article.doi,
                'pmid': article.pmid,
                'pmc': article.pmc,
                'pub_year': article.pub_year
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
        })
        
    def as_json(self):
        return {
            'title': self.title,
            'abstract': self.abstract,
            'is_peer_reviewed': self.is_peer_reviewed,
            'metadata': self.metadata
        }