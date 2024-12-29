# Litocate

Automatic literature locator that scans [PubMed](https://pubmed.ncbi.nlm.nih.gov/) and [ACL Anthology](https://aclanthology.org/).

## Get Started

```
poetry install
```

## Example Usage

### PubMed

```python
from litocate.data.pubmed import PubMedClient
from litocate.data.constant import PUBMED_FOLDERS

results = []

# Pubmed stores their articles across multiple folders 
# based on their license 
for pubmed_folder in PUBMED_FOLDERS: 
    pubmed_result = PubMedClient(
        folder=pubmed_folder    
    ).find_papers(
        keywords=['medical'],
        pub_after_year=2023,
        max_threads=32,
        n=2
    )
    results.extend(pubmed_result)

print(results[0].title, results[0].abstract)
```

### ACL Anthology

```python
acl_result = AnthologyClient().find_papers(
    keywords=['medical'], 
    pub_after_year=2023,
    n=2
)
print(acl_result[0].title, acl_result[0].abstract)
```

## Developer Guide

To run unit test, 

```
poetry run pytest
```