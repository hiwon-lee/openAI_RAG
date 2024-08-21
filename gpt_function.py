# gpt_functions.py
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
# from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document


def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size = 500,
    #     chunk_overlap = 0
    # )
    return text_splitter.split_documents(documents)


# from halo import Halo

# 필요하다면, 여기서 vector_database와 llm을 설정합니다.
# 예: vector_database = ...
# 예: llm = ChatOpenAI(api_key=api_key, model_name="gpt-4o", temperature=0)
load_dotenv(
    dotenv_path='.env',
    verbose=True,
)
api_key = os.environ.get("OPEN_API_KEY")
client = OpenAI(api_key=api_key)
llm = ChatOpenAI(api_key=api_key, model_name="gpt-4o", temperature=0)
chain = load_qa_chain(llm, chain_type="stuff",verbose=True)
# 프롬프트 파일 경로
prompt = "prompt/qa_chain_prompt.txt"
DATA_PATH = "ragData"
document_loader = PyPDFDirectoryLoader(DATA_PATH)
documents = document_loader.load()
# print(documents)
QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt)
# embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
chunks = split_documents(documents)

vector_database = Chroma.from_documents(documents = chunks, embedding = embeddings)

# question = input()

def gpt_llm(query):
    # 여기에 RetrievalQA 설정 및 실행 코드가 포함됩니다.
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_database.as_retriever(),
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    retrieved_docs = vector_database.similarity_search(query, k=7)  # 가장 관련성 높은 문서 검색

    context = ""
    if retrieved_docs:
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    input_data = {"context": context, "query": query}
    result = qa_chain(input_data)

    return result["result"]

def rag_chain(query):
    retriever = vector_database.as_retriever()
    retrieved_docs = retriever.invoke(query)
    return gpt_llm(query)

def get_important_facts(query):
    return rag_chain(query)

# def generate_response(messages):
#     spinner = Halo(text='Loading...', spinner='dots')
#     spinner.start()

question = input("써라")
# 더 필요한 함수들이 있다면 여기에 정의합니다.
xmlresult = get_important_facts(question)

print(xmlresult)