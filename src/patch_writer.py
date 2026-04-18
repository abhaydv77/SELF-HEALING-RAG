from groq import Groq
import os
from dotenv import load_dotenv
import re
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PATCH_PROMPT = PATCH_PROMPT = """You are a document editor. Fix the following text based on the issue described.
ORIGINAL TEXT:
{original_text}

ISSUE TYPE: {issue_type}
ISSUE DESCRIPTION: {description}

Rules:
- Fix ONLY the specific issue mentioned
- Keep everything else exactly the same
- Do not add new information
- Return ONLY the fixed text, nothing else
"""

def write_patch(original_text,issue):
    prompt = PATCH_PROMPT.format(
        original_text=issue["text"], 
        issue_type=issue["issue_type"],
        description=issue["description"]

    )

    response= client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    fixed_text = response.choices[0].message.content.strip()
    print(f"FIXED TEXT FROM LLM:\n{fixed_text}\n")
    return {
     "original": issue["text"],     
        "fixed": fixed_text,           
        "issue_type": issue["issue_type"],
        "description": issue["description"],
        "severity": issue["severity"]
}

def generate_patches(original_text, issues):
    patches = []
    current_text = original_text
    
    
    valid_issues = [issue for issue in issues if issue.get("issues_found", False)]
    
    if not valid_issues:
       
        return [], original_text
    
    for issue in valid_issues:
        patch = write_patch(current_text, issue)
        patches.append(patch)
        current_text = current_text.replace(
            patch["original"],
            patch["fixed"]
        )
    
    return patches, current_text



if __name__ == "__main__":
    from llm_analyser import analyse_chunk
    test_chunk = """
    Machine learning was invented in 2001 by Geoffrey Hinton.
    Neural networks are used for many tasks. Neural networks 
    are used for many different tasks in AI systems.
    The backpropagation algorithm was developed in 2015.
    """
    print("Analysing...")
    issues = analyse_chunk(test_chunk)

    print(f"\nFound {len(issues)} issues. Generating patches...")
    patches,fixed_text = generate_patches(test_chunk, issues)

    print("\n--- ORIGINAL TEXT ---")
    print(test_chunk)
    print("\n--- FIXED TEXT ---")
    print(fixed_text)
    print("\n--- PATCHES LOG ---")
    for i, patch in enumerate(patches):
        print(f"\nPatch {i+1}: {patch['issue_type']}")
        print(f"Issue: {patch['description'][:100]}...")
            