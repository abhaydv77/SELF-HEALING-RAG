from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PATCH_PROMPT = """You are a document editor. Fix the following text based on ONLY this specific issue.

TEXT:
{original_text}

ISSUE: {description}

RULES:
- Fix ONLY this one issue
- Change nothing else
- Keep exact format and length close to original
- Return ONLY the corrected text

CORRECTED TEXT:"""

def write_patch(original_text, issue):
    # ✅ Use full text for context
    prompt = PATCH_PROMPT.format(
        original_text=original_text,
        description=issue["description"]
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )

    fixed_text = response.choices[0].message.content.strip()
    
    return {
        "original": original_text,
        "fixed": fixed_text,
        "issue_type": issue["issue_type"],
        "description": issue["description"],
        "severity": issue["severity"]
    }

def generate_patches(original_text, issues):
    """Generate patches for each issue sequentially"""
    patches = []
    current_text = original_text
    
    print(f"\n📋 Processing {len(issues)} issues...")
    
    for idx, issue in enumerate(issues, 1):
        print(f"\n[{idx}] Fixing {issue['issue_type']}: {issue['description'][:60]}...")
        
        patch = write_patch(current_text, issue)
        patches.append(patch)
        
        # ✅ Update text for next iteration
        current_text = patch["fixed"]
        print(f"    ✓ Applied patch {idx}/{len(issues)}")
    
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
    
    if issues:
        print(f"\nFound {len(issues)} issues. Generating patches...")
        patches, fixed_text = generate_patches(test_chunk, issues)
        
        print("\n" + "="*60)
        print("ORIGINAL:")
        print(test_chunk)
        print("\n" + "="*60)
        print("FIXED:")
        print(fixed_text)
        print("\n" + "="*60)
        print(f"Total patches applied: {len(patches)}")
    else:
        print("No issues found!")