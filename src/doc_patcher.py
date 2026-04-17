import os 
import json
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

PATCH_LOG_PATH = "./logs/patch_log.json"

def save_to_files(file_path, fixed_text):
    with open(file_path,'w',encoding='utf-8')as f:
        f.write(fixed_text)
    print(f"Fixed text saved to {file_path}")    


def load_patch_log():
    if os.path.exists(PATCH_LOG_PATH):
        with open(PATCH_LOG_PATH,'r',encoding='utf-8')as f:
            return json.load(f)
    return []

def save_patch_log(file_path,patches,original_text):
    log = load_patch_log()
    
    if not isinstance(patches, list):
        raise TypeError(f"Expected patches to be a list, got {type(patches).__name__}")

    formatted_patches = []
    for p in patches:
        if not isinstance(p, dict):
            raise TypeError(f"Expected each patch to be a dict, got {type(p).__name__}")
        formatted_patches.append({
            "issue_type": p["issue_type"],
            "description": p["description"],
            "severity": p["severity"],
            "before": (p.get("original") or p.get("before", ""))[:200],
            "after": (p.get("fixed") or p.get("after", ""))[:200]
        })

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": file_path,
        "total_patches": len(patches),
        "patches": formatted_patches
    }


    log.append(log_entry)

    os.makedirs("./logs",exist_ok=True)
    with open(PATCH_LOG_PATH,'w',encoding='utf-8')as f:
        json.dump(log,f,indent=4)
    print(f"Patch log saved: {len(patches)} patches logged") 



def apply_patches(file_path, patches, original_text,final_text)  :
    
    save_to_files(file_path, final_text)

    save_patch_log(file_path, patches, original_text)

    return{
        "file_path": file_path,
        "patches_applied": len(patches),
        "status":"healed"

    }


if __name__ == "__main__":
    from llm_analyser import analyse_chunk
    from patch_writer import generate_patches
    
    # test
    test_file = "./data/raw_docs/test.txt"
    test_text = """
    Machine learning was invented in 2001 by Geoffrey Hinton.
    Neural networks are used for many tasks. Neural networks 
    are used for many different tasks in AI systems.
    The backpropagation algorithm was developed in 2015.
    """

    with open(test_file,'w')as f:
        f.write(test_text)
    
    print("Analysing...")   
    issues = analyse_chunk(test_text)

    print(f"{len(issues)} issue found. Generating patches...")
    patches,fixed_text= generate_patches(test_text, issues)

    result= apply_patches(test_file, patches, test_text, fixed_text)
    print(f"\n result: {result}")


    print("\n patch log:")
    log = load_patch_log()
    if log:
     print(json.dumps(log[-1], indent=2))
    else:
        print("No log entries found.")


          
 



