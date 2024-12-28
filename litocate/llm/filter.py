import os

import getpass
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

class Classification(BaseModel):
    relevant: bool = Field(description="Whether the passage is relevant given the prompt")

class LLMClassifier:
    
    def __init__(self, prompt):
        self.llm = ChatOpenAI(model="gpt-4o").with_structured_output(
            Classification
        )
        self.tagging_prompt = ChatPromptTemplate.from_template(prompt)

    def classify(self, passage: str):
        prompt = self.tagging_prompt.invoke(input=passage)
        return self.llm.invoke(prompt)


if __name__ == "__main__":

    classify_prompt ="""
    Identify and review passage to determine if it is related to biomedical/healthcare text simplification that use Large Language Model, or Natural Language Processing techniques, focusing on methods (including automated evaluation), datasets (e.g., PubMed, clinical notes, UMLS), target audiences (patients, professionals), and measurable impact on readability and real-world usability.

    Passage:
    {input}
    """
    classifier = LLMClassifier(classify_prompt)
    passage = 'Improved readability and functions needed for mHealth apps targeting patients with heart failure: An app store review'
    assert classifier.classify(passage).relevant == True
    
    passage =  'Evaluation of Available Online Information Regarding Treatment for Vitreous Floaters'
    assert classifier.classify(passage).relevant == False
