import json
import datetime
import logging
import concurrent.futures
from tqdm import tqdm

import boto3
from botocore.config import Config
from botocore import UNSIGNED
from lxml import etree

from litocate.data.utils import keyword_exist
from litocate.data.base import Paper
from litocate.data.constant import DS_FORMAT

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


ABSTRACT_TAG = 'abstract'
MAX_POOL_CONNECTIONS = 1000

class PubMedClient:
    def __init__(self, folder=None):
        self.s3 = boto3.client('s3', config=Config(
                signature_version=UNSIGNED, 
                max_pool_connections=MAX_POOL_CONNECTIONS
            )
        )
        self.bucket_name = 'pmc-oa-opendata'
        self.folder = folder if folder else 'oa_comm'
        self.prefix = f'{folder}/xml/all'

    def get(self, key):        
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            return response['Body'].read()
        except Exception as e:
            logger.error(f"Error downloading file: {e}", exc_info=True)
            return None


    def _find_papers(self, obj_key, keywords, pub_after_year):
        xml_str = self.get(obj_key)
        title_match, abstract_match = False, False
        
        try:
            xml_obj = PubMedArticle.from_string(xml_str)
        except Exception as e:
            logger.error(f"Error parsing XML: {e}", exc_info=True)
            return None

        if xml_obj._content is None:
            return None
        if xml_obj.pub_year is None:
            return None
        elif xml_obj.pub_year is None or (
            pub_after_year is not None and int(xml_obj.pub_year) < pub_after_year
        ):
            return None

        if xml_obj.title:
            content = xml_obj.title
            title_match = keyword_exist(content, keywords)
        if xml_obj.abstract:
            content = " ".join(xml_obj.abstract.values())
            abstract_match = keyword_exist(content, keywords)

        if title_match or abstract_match:
            return Paper.from_pubmed_article(xml_obj)
        return None

    def find_papers(self, keywords, pub_after_year=2021, max_threads=MAX_POOL_CONNECTIONS, n=None):
        papers = []
        
        try:
            paginator = self.s3.get_paginator('list_objects_v2')
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:

                futures = []
                total_files = 0
                
                for page in paginator.paginate(Bucket=self.bucket_name, Prefix=self.prefix):
                    if 'Contents' not in page:
                        logger.info("No files found in the bucket.")
                        continue
                    if n and total_files >= n:
                        break
                    
                    total_files += len(page['Contents'])
                    for obj in page['Contents']:
                        futures.append(
                            executor.submit(self._find_papers, obj['Key'], keywords, pub_after_year)
                        )

                with tqdm(total=total_files, desc="Processing files") as pbar: 
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            result = future.result()
                            if result:
                                papers.append(result)
                        except Exception as e:
                            logger.error(f"Error processing a file: {e}", exc_info=True)
                        finally:
                            pbar.update(1)  # Update progress bar after each task
            return papers

        except Exception as e:
            logger.error(f"Error in listing files: {e}", exc_info=True)
            return []

    def get_metadata_file(self):
        import pandas as pd
        from io import BytesIO
        key = f'{self.folder}/xml/metadata/csv/{self.folder}.filelist.csv'
        csv_bytes = self.get(key)
        df = pd.read_csv(BytesIO(csv_bytes))
        return df 
    
    def find_papers_updated_after(self, datetime_str, keywords, pub_after_year):
        import pandas as pd
        try:
            last_updated = datetime.datetime.strptime(datetime_str, DS_FORMAT)
        except Exception as e:
            raise Exception(
                f'Error in parsing datetime string {e} - Expect format {DS_FORMAT}'
            )
        DATE_COLUMN = 'Last Updated UTC (YYYY-MM-DD HH:MM:SS)'
        df = self.get_metadata_file()
        df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN])
        papers = []
        for key in df[df[DATE_COLUMN] > last_updated]['Key'].tolist():
            paper = self._find_papers(key, keywords, pub_after_year)
            if paper:
                papers.append(paper)
        return papers

class PubMedArticle:
    
    def __init__(self, xml_str):
        self._content = self.str2xml(xml_str)
        if self._content is not None:
            self.abstract = self.get_abstract_from_xml(self._content)
            self.title = self.get_title(self._content)
            self.doi = self.get_article_id(self._content)
            self.pmid = self.get_article_id(self._content, type='pmid')
            self.pmc = self.get_article_id(self._content, type='pmc')
            self.pub_year = self.get_pub_year(self._content)
            self.peer_reviewed = self.is_peer_reviewed(self._content)
        else:
            self.abstract = None
            self.title = None
            self.doi = None
            self.pmid = None
            self.pmc = None
            self.pub_year = None
            self.peer_reviewed = None

    @classmethod
    def from_string(cls, xml_str):
        return cls(xml_str)

    @classmethod
    def from_s3_key(cls, s3_key):
        xml_str = PubMedClient().get(s3_key)
        return cls(xml_str)

    @staticmethod
    def get_article_id(xml, type='doi'):
        article_id_element = xml.xpath(f"//article-id[@pub-id-type='{type}']")
        if article_id_element:
            return article_id_element[0].text

    @staticmethod
    def get_abstract_from_xml(xml):
        abstracts = xml.xpath(f'//{ABSTRACT_TAG}')
        for abstract in abstracts:
            # Only go with the first abstract, which is the full one. 
            abstract_dict = PubMedArticle.abstract_to_dict(abstract)
            return abstract_dict
    
    @staticmethod
    def str2xml(xml_str):
        try:
            return etree.fromstring(xml_str)
        except Exception as e:
            logger.debug(f"Error parsing XML: {e}", exc_info=True)
            return None

    @staticmethod
    def get_title(element):
        title_elements = element.xpath('//front//article-title')
        if title_elements is None:
            return 
        for title_element in title_elements:
            try:
                return "".join(title_element.itertext()).strip()
            except Exception as e:
                logger.debug(f"Error getting title: {e}", exc_info=True)
                pass
        return None

    @staticmethod
    def get_pub_year(element):
        year_element = element.xpath(".//pub-date/year")
        if year_element:
            return year_element[0].text 

    @staticmethod
    def abstract_to_dict(element):
        result = {}
        title_element_name = 'title'
        outer_title_element = element.find(title_element_name)
        if outer_title_element is not None:
            key_text = outer_title_element.text
            if key_text:
                result[title_element_name] = outer_title_element.text.strip()

        for i, p in enumerate(element.xpath('p')):
            result[f'{title_element_name}_content_{i}'] = "".join(p.itertext()).strip()

        for sec in element.xpath('./sec'):
            title_element = sec.find('title')
            key = title_element.text.strip() if title_element is not None and title_element.text else None
            # Gather all text within <p> and its children
            value = ''.join(sec.xpath('.//p//text()')).strip() 
            if key:
                result[key] = value
        return result

    @staticmethod
    def is_peer_reviewed(xml):
        journals = xml.xpath("//journal-meta")
        return True if journals else False