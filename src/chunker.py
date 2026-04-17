import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict

from doc_loader import load_all_docs


def chunk_docs():
 splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

 chunks = splitter.split_documents(load_all_docs())
 print(f"Total chunks created: {len(chunks)}")
 print(chunks[0])
 print("---")
 print(chunks[0].page_content)  # text
 print(chunks[0].metadata) 

 return chunks
 

if __name__ == "__main__":
    chunk_docs()



 