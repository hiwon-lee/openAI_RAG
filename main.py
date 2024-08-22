from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from openai import OpenAI
import bs4
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv(
    dotenv_path='.env',
    verbose=True,
)

api_key = os.environ.get("OPEN_API_KEY")
PROMPT_PATH = "prompt/qa_chain_prompt.txt"
DATA_PATH = "ragData"
document_loader = PyPDFDirectoryLoader(DATA_PATH)
documents = document_loader.load()


client = OpenAI(api_key=api_key)

llm = ChatOpenAI(api_key=api_key, model_name="gpt-4o", temperature=0)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
retriever = vectorstore.as_retriever()

# 파일 내용을 읽어서 system_prompt 변수에 저장
# 파일 내용을 읽어서 system_prompt 변수에 저장 (UTF-8 인코딩 지정)
with open(PROMPT_PATH, 'r', encoding='utf-8') as file:
    system_prompt = file.read()
    
# print(system_prompt)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "{question}"),
    ]
)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# This Runnable takes a dict with keys 'input' and 'context',
# formats them into a prompt, and generates a response.
rag_chain_from_docs = (
    {
        "input": lambda x: x["input"],  # input query
        "context": lambda x: format_docs(x["context"]),  # context
    }
    | prompt  # format query and context into prompt
    | llm  # generate response
    | StrOutputParser()  # coerce to string
)

# Pass input query to retriever
retrieve_docs = (lambda x: x["input"]) | retriever

# Below, we chain `.assign` calls. This takes a dict and successively
# adds keys-- "context" and "answer"-- where the value for each key
# is determined by a Runnable. The Runnable operates on all existing
# keys in the dict.
chain = RunnablePassthrough.assign(context=retrieve_docs).assign(
    answer=rag_chain_from_docs
)

chain.invoke({"input": "What is Task Decomposition"})