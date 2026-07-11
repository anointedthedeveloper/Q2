import json
import os
from pathlib import Path

def clean_explanations_in_json(file_path):
    """Remove 'click here' from explanation fields in a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        modified = False
        count = 0
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'explanation' in item:
                    if item['explanation'] and 'click here' in item['explanation'].lower():
                        item['explanation'] = ""
                        modified = True
                        count += 1
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[OK] Cleaned {count} explanations in {file_path.name}")
            return count
        else:
            print(f"[--] No 'click here' explanations found in {file_path.name}")
            return 0
            
    except Exception as e:
        print(f"[ERROR] Error processing {file_path.name}: {e}")
        return 0

def main():
    # Get all JSON files in the current directory
    directory = Path(__file__).parent
    json_files = list(directory.glob('*.json'))
    
    print(f"Found {len(json_files)} JSON files to process...\n")
    
    total_cleaned = 0
    for json_file in json_files:
        total_cleaned += clean_explanations_in_json(json_file)
    
    print(f"\nTotal explanations cleaned: {total_cleaned}")

if __name__ == "__main__":
    main()
