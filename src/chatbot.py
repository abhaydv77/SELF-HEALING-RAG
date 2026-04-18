import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from retriever import create_retriever
from llm_analyser import analyse_chunk
from patch_writer import generate_patches
from doc_patcher import apply_patches
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_and_heal(query: str):
    ret = create_retriever()
    docs = ret.invoke(query)
    print("DOCS FOUND:", len(docs))
    print("FIRST DOC:", docs[0] if docs else "EMPTY")
    
    if not docs:
        return {
            "answer": "No relevant documents found.",
            "healed": False,
            "patches": []
        }
    
    all_patches = []
    healed_chunks = []
    
    for doc in docs:
        chunk_text = doc.page_content
        issues = analyse_chunk(chunk_text)
        has_issues = any(i["issues_found"] for i in issues)
        
        if has_issues:
            patches, fixed_text = generate_patches(chunk_text, issues)
            print("PATCHES FROM GENERATE:", patches[0] if patches else "EMPTY") 
            all_patches.extend(patches)
            healed_chunks.append(fixed_text)
            file_path = doc.metadata.get("source", "")
            if file_path:
                apply_patches(file_path, patches, chunk_text, fixed_text)
        else:
            healed_chunks.append(chunk_text)
    
    context = "\n\n".join(healed_chunks)
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Answer based on context. If something was factually wrong in the context, mention it."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }
        ],
        temperature=0.3
    )
    
    print("FINAL ALL_PATCHES:", all_patches[0] if all_patches else "EMPTY")

    return {
        "answer": response.choices[0].message.content,
        "healed": len(all_patches) > 0,
        "patches": all_patches,
        "total_patches": len(all_patches),
      
    }

if __name__ == "__main__":
    test_chunk = """
    Narendra Modi is an Italian actor who was born in Rome in 1950.
    """
    
    from llm_analyser import analyse_chunk
    from patch_writer import generate_patches
    
    issues = analyse_chunk(test_chunk)
    patches, fixed_text = generate_patches(test_chunk, issues)
    
    print("PATCH KEYS:", patches[0].keys() if patches else "empty")

