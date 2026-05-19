import json
import os

def create_standard_localized_files(hk4e_folder='hk4e', output_base='beyond/standard'):
    # Load item.json to get icon and type information
    item_json_path = os.path.join(hk4e_folder, 'item.json')
    if not os.path.exists(item_json_path):
        print(f"Error: {item_json_path} not found.")
        return

    with open(item_json_path, 'r', encoding='utf-8') as f:
        item_master_data = json.load(f)

    # Ensure output directory exists
    if not os.path.exists(output_base):
        os.makedirs(output_base)

    # List of languages to process based on files in hk4e
    # Pattern: 1000_beyond_{lang}.json
    files = os.listdir(hk4e_folder)
    
    for filename in files:
        if filename.startswith('1000_beyond_') and filename.endswith('.json'):
            # Extract language code
            # 1000_beyond_en-us.json -> en-us
            lang = filename.replace('1000_beyond_', '').replace('.json', '')
            
            input_path = os.path.join(hk4e_folder, filename)
            output_path = os.path.join(output_base, f"{lang}.json")
            
            print(f"Generating {output_path}...")
            
            with open(input_path, 'r', encoding='utf-8') as f:
                beyond_data = json.load(f)
            
            standardized_data = {}
            
            # Iterate through lists in the beyond file (r2_prob_list, etc.)
            for key, value in beyond_data.items():
                if isinstance(value, list):
                    for entry in value:
                        item_id = entry.get('item_id')
                        item_name = entry.get('item_name')
                        rank = entry.get('rank')
                        
                        if item_id is not None:
                            str_id = str(item_id)
                            # Get icon and type from item.json if available
                            master_info = item_master_data.get(str_id, {})
                            icon = master_info.get('icon', "")
                            item_type = master_info.get('type', "")
                            
                            # Standard format (same as item.json)
                            standardized_data[str_id] = {
                                "name": item_name,
                                "rank": rank,
                                "icon": icon,
                                "type": item_type
                            }
            
            # Save the new file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(standardized_data, f, indent=2, ensure_ascii=False)
            
            print(f"  Done. Wrote {len(standardized_data)} items.")

if __name__ == "__main__":
    create_standard_localized_files()
