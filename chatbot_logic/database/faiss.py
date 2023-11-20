import os
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
import numpy as np
from logger import get_logger
from langchain.embeddings import HuggingFaceEmbeddings

logger = get_logger(__name__)

# Initialize the Sentence Transformer Model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

with open(r'./database/processed_korquad.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Split the content into chunks and embed
query_result = embeddings.embed_query(content)


faissdb = FAISS.from_texts(content, embeddings)
query = "what is the question?"
docs_and_scores = faissdb.similarity_search_with_score(query)
docs_query = faissdb.similarity_search(query)
embedding_vector = embeddings.embed_query(query)
docs_and_scores = faissdb.similarity_search_by_vector(embedding_vector)
faissdb.save_local("faiss_index")

faissdb = FAISS.from_texts(content, embeddings, "faiss index")

# Concatenate encoded_chunk
# Create a FAISS index
 # Add document encoded_chunk to the index

# Assuming you need a function to initialize the FAISS index
def get_faiss():
        faissdb = FAISS(
            collection_name='llm',
            embedding_function=embeddings,
            persist_directory='./faiss.db'
        )
        return faissdb