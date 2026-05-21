import json
import shutil
import os

def main():
    json_file_path = 'beyond/limited/en-us.json'
    source_dir = 'export/Texture2D'
    dest_dir = 'assets'

    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    # Load the JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Keep track of icons we've already attempted to copy to avoid duplicate work
    processed_icons = set()

    # Iterate through all items in the JSON
    for item_id, item_info in data.items():
        icon_name = item_info.get('icon')
        
        if icon_name and icon_name not in processed_icons:
            source_path = os.path.join(source_dir, f"{icon_name}.png")
            dest_path = os.path.join(dest_dir, f"{icon_name}.png")
            
            # Copy the file if it exists
            if os.path.exists(source_path):
                try:
                    shutil.copy2(source_path, dest_path)
                    print(f"Copied: {icon_name}.png")
                except Exception as e:
                    print(f"Error copying {icon_name}.png: {e}")
            else:
                print(f"Not found in source: {icon_name}.png")
            
            processed_icons.add(icon_name)

if __name__ == '__main__':
    main()
