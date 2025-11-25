from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from langserve import add_routes  ##helps in creating apis
from dotenv import load_dotenv
load_dotenv()

model=Ollama(model="gemma:2b")

#1. Create prompt template
system_template="You are a translator. Translate the following text into {language}. Provide only the translation, nothing else."
prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system",system_template),
        ("user","{text}")
    ]
)
parser=StrOutputParser()

#Chain
chain=prompt_template|model|parser

##App Definition
app=FastAPI(title="Langchain Server",
            version="1.0",
            description="A simple API server using Langchain runnable interface")


add_routes(app,
           chain,
           path="/chain")

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)