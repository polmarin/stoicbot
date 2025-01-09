import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

from constants import DB_PATH, DATA_PATH

def store_data(data_path, db_path):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    embeddings = HuggingFaceEmbeddings()
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)

    for filename in os.listdir(data_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_path, filename)
            with open(file_path, "r") as file:
                content = file.read()
                texts = text_splitter.split_text(content)
                vector_db.add_texts(texts)

    vector_db.persist()
    print("Data stored successfully")

if __name__ == "__main__":
    store_data(DATA_PATH, DB_PATH)
