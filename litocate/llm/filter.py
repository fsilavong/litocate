import os

import getpass
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from litocate.llm.prompts import classify_prompt

if not os.environ.get("OPENAI_API_KEY"):
  os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

class Classification(BaseModel):
    relevant: bool = Field(description="Whether the passage is relevant given the prompt")

class LLMClassifier:
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(
            Classification
        )
        self.tagging_prompt = ChatPromptTemplate.from_template(classify_prompt)

    def classify(self, passage: str):
        prompt = self.tagging_prompt.invoke(input=passage)
        return self.llm.invoke(prompt)


if __name__ == "__main__":
    classifier = LLMClassifier()
    passage = 'Improved readability and functions needed for mHealth apps targeting patients with heart failure: An app store review'
    assert classifier.classify(passage).relevant == True
    
    passage =  'Evaluation of Available Online Information Regarding Treatment for Vitreous Floaters'
    assert classifier.classify(passage).relevant == False
