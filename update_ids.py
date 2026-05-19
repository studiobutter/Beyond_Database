import json
import os

def update_item_ids(beyond_path, item_path):
    # Load item.json and create name to id mapping
    with open(item_path, 'r', encoding='utf-8') as f:
        items_data = json.load(f)
    
    name_to_id = {}
    for item_id, item_info in items_data.items():
        name = item_info.get('name')
        if name:
            # We store the ID. If it's numeric, we'll try to keep it as int if possible, 
            # but usually JSON keys are strings. 
            # We'll see if we should convert it to int.
            try:
                name_to_id[name] = int(item_id)
            except ValueError:
                name_to_id[name] = item_id

    # Load 1000_beyond.json
    with open(beyond_path, 'r', encoding='utf-8') as f:
        beyond_data = json.load(f)

    def process_list(item_list):
        updated_count = 0
        for item in item_list:
            name = item.get('item_name')
            if name in name_to_id:
                old_id = item.get('item_id')
                new_id = name_to_id[name]
                if old_id != new_id:
                    item['item_id'] = new_id
                    updated_count += 1
        return updated_count

    total_updated = 0
    # Search for all lists in the beyond_data
    for key, value in beyond_data.items():
        if isinstance(value, list):
            total_updated += process_list(value)

    # Save the updated beyond file
    with open(beyond_path, 'w', encoding='utf-8') as f:
        json.dump(beyond_data, f, indent=4, ensure_ascii=False)

    print(f"Updated {total_updated} items in {beyond_path}")

if __name__ == "__main__":
    beyond_file = os.path.join('hk4e', '2000_beyond_en-us.json')
    item_file = os.path.join('hk4e', 'item.json')
    
    if os.path.exists(beyond_file) and os.path.exists(item_file):
        update_item_ids(beyond_file, item_file)
    else:
        print("Required files not found.")
