import os
from dotenv import load_dotenv
from langchain_mistralai import MistralAIEmbeddings
from langchain_chroma import Chroma



load_dotenv()
CHROMA_PATH = os.getenv("CHROMA_PATH")

def create_retriever():
   embedding_model = MistralAIEmbeddings(model="mistral-embed")
   vectorstore = Chroma(
      embedding_function=embedding_model,
      persist_directory=CHROMA_PATH,
      collection_name="my_collection"
    )
   retrievers = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
           "k": 5,
           "fetch_k": 10,
           "lambda_mult": 0.5

          }
        )
   return retrievers

if __name__ == "__main__":
    retriever = create_retriever()
    print("Retriever created successfully")

   
# test query
results = retriever.invoke("what is machine learning?")
    
for i, doc in enumerate(results):
        print(f"\n--- Chunk {i+1} ---")
        print(doc.page_content[:200])  
        print(f"Source: {doc.metadata}")