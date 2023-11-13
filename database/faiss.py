import os
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from logger import get_logger
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader


logger = get_logger(__name__)

embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
if os.getenv('OPENAI_API_TYPE') == 'azure':
    embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), deployment=os.getenv(
        "OPENAI_API_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002"), chunk_size=1)


# 파이스로 집어넣는거 새로 작업중
#loader = TextLoader("../../../extras/modules/state_of_the_union.txt")
#documents = loader.load()
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#docs = text_splitter.split_documents(documents)

###########################################
#db = FAISS.from_documents(docs, embeddings)
#query = "What did the president say about Ketanji Brown Jackson"
#docs = db.similarity_search(query)
################

def get_chroma():
    chroma = Chroma(
        collection_name='llm',
        embedding_function=embedding,
        persist_directory='./chroma.db'
    )
    return chroma
