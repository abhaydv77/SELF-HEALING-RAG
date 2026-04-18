from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

ANALYSIS_PROMPT = """Analyze this text for issues:
{chunk_text}

Respond with:
ISSUES_FOUND: yes/no
ISSUE_TYPE: wrong_fact/redundancy/unclear/bad_code/none
DESCRIPTION: what is wrong
SEVERITY: high/medium/low"""

def analyse_chunk(chunk_text):
    prompt = ANALYSIS_PROMPT.format(chunk_text=chunk_text)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    raw_text = response.choices[0].message.content
    return parse_analysis(raw_text)


def parse_analysis(raw_text):
    
    blocks = raw_text.strip().split('---')
    
    issues = []
    
    for block in blocks:
        current = {}
        for line in block.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                current[key.strip()] = value.strip()
        
        if current.get('ISSUE_TYPE') and current.get('ISSUE_TYPE').lower() != 'none':
            issues.append({
                "issues_found": True,
                "issue_type": current.get('ISSUE_TYPE', 'none'),
                "description": current.get('DESCRIPTION', ''),
                "severity": current.get('SEVERITY', 'low'),
                "text": ""
            })
    
    if not issues:
        return [{
            "issues_found": False,
            "issue_type": "none",
            "description": "",
            "severity": "low",
            "text": ""
        }]
    
    return issues


if __name__ == "__main__":
    test_chunk = """
    Machine learning was invented in 2001 by Geoffrey Hinton.
    Neural networks are used for many tasks. Neural networks 
    are used for many different tasks in AI systems.
    The backpropagation algorithm was developed in 2015.
    """
    
    result = analyse_chunk(test_chunk)
    for i, issue in enumerate(result):
        print(f"\n---- Issue {i+1} ----")
        print(issue)