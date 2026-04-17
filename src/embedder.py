import os
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from chunker import chunk_docs
from langchain_community.vectorstores import Chroma

load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")


def create_vector_store():
    chunks = chunk_docs()
    print(f"Creating embeddings for {len(chunks)} chunks...")
    embedding_model = MistralAIEmbeddings(
        model="mistral-embed",
        api_key=os.getenv("MISTRAL_API_KEY")
        )
    vector_store = Chroma.from_documents(
       
        documents = chunks,
        embedding=embedding_model,
        collection_name="my_collection",
        persist_directory=CHROMA_PATH
    )
    print("vector store created")
    return vector_store


if __name__ == "__main__":
    create_vector_store()


    

