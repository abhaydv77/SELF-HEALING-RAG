import argparse
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from llm_analyser import analyse_chunk
from patch_writer import generate_patches
from doc_patcher import apply_patches

print(" CLI FILE STARTED")

def main():
    parser = argparse.ArgumentParser(
        description="Self-Healing Document Tool"
    )

    parser.add_argument(
        "file",
        type=str,
        help="Path to input file"

    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="show change without saving"
    )
    args = parser.parse_args()
    with open(args.file, 'r', encoding='utf-8') as f:
        text = f.read()
    print("Analysing...")    
    issues = analyse_chunk(text)

    print(f" {len(issues)} issues found. Generating patches...")
    patches, fixed_text = generate_patches(text, issues)

    if args.preview:
        print("\n--- PREVIEW ---")
        print(fixed_text)
        return
    
    result = apply_patches(args.file, patches, text, fixed_text)
    print(f"\n result: {result}")

if __name__ == "__main__":
    main()    





