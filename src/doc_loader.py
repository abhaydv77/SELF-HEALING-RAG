import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document


load_dotenv()
DOCS_PATH = os.getenv("DOCS_PATH")

def load_all_docs():
    all_docs = []
    
    for file in Path(DOCS_PATH).iterdir():
        ext = file.suffix.lower()
        
        try:
            if ext == '.pdf':
                loader = PyPDFLoader(str(file))
                docs = loader.load()
                
            elif ext == '.docx':
                loader = Docx2txtLoader(str(file))
                docs = loader.load()
                
            elif ext in ['.txt', '.md', '.py']:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                docs = [Document(page_content=content, metadata={"source": str(file)})]
                
            else:
                print(f"Skipping unsupported file: {file.name}")
                continue
                
            all_docs.extend(docs)
            print(f"Loaded: {file.name}")
            
        except Exception as e:
            print(f"Error loading {file.name}: {e}")
            continue
    
    return all_docs

if __name__ == "__main__":
    docs = load_all_docs()
    print(f"\nTotal documents loaded: {len(docs)}")