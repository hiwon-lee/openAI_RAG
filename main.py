import json
import os
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI  # ChatOpenAI를 사용할 경우
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate




# 객체 내용 출력 유틸
def show_json(obj):
  display(json.loads(obj.model_dump_json()))

def _get_response(thread_id):
    return client.beta.threads.messages.list(thread_id=thread_id, order="asc")

# Thread message 출력 유틸
def print_message(thread_id):
    for res in _get_response(thread_id):
        print(f"[{res.role.upper()}]\n{res.content[0].text.value}\n")