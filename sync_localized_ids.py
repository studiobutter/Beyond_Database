import json
import os

def sync_localized_ids(base_file, lang_list, folder='hk4e'):
    # Load base English file and create mapping from order_value to item_id
    base_path = os.path.join(folder, base_file)
    if not os.path.exists(base_path):
        print(f"Base file {base_path} not found.")
        return

    with open(base_path, 'r', encoding='utf-8') as f:
        base_data = json.load(f)

    # We need to map order_value -> item_id for each rank list
    # Since order_value might not be unique across all lists (r2, r3, r4), 
    # we should index them by list key if possible, or just build a global map if they are unique.
    # Looking at the previous reads, order_value seems to be distinct within each rank list at least.
    
    order_map = {} # (list_key, order_value) -> item_id
    for key, value in base_data.items():
        if isinstance(value, list):
            for item in value:
                ov = item.get('order_value')
                iid = item.get('item_id')
                if ov is not None:
                    order_map[(key, ov)] = iid

    # Iterate through each language
    for lang in lang_list:
        lang_file = f"2000_beyond_{lang}.json"
        lang_path = os.path.join(folder, lang_file)
        
        if not os.path.exists(lang_path):
            # Skip silently or notify? The prompt asks to make it compatible, 
            # so we'll check if they exist.
            continue
        
        print(f"Processing {lang_path}...")
        with open(lang_path, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        updated_count = 0
        for key, value in lang_data.items():
            if isinstance(value, list):
                for item in value:
                    ov = item.get('order_value')
                    if ov is not None and (key, ov) in order_map:
                        new_id = order_map[(key, ov)]
                        if item.get('item_id') != new_id:
                            item['item_id'] = new_id
                            updated_count += 1
        
        if updated_count > 0:
            with open(lang_path, 'w', encoding='utf-8') as f:
                json.dump(lang_data, f, indent=2, ensure_ascii=False)
            print(f"  Updated {updated_count} items in {lang_path}")
        else:
            print(f"  No updates needed for {lang_path}")

if __name__ == "__main__":
    languages = [
        "de-de", "es-es", "fr-fr", "id-id", "it-it", "ja-jp", 
        "ko-kr", "pt-pt", "ru-ru", "th-th", "tr-tr", "vi-vn", 
        "zh-cn", "zh-tw"
    ]
    sync_localized_ids("2000_beyond_en-us.json", languages)
