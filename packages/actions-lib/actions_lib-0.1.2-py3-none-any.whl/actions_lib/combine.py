import os
import json

def combine_json_files(root_dir, output_file):
    combined_data = []

    for subdir, dirs, files in os.walk(root_dir):
        # subdir_name = os.path.basename(subdir)
        """ai.json"""
        json_file_name = f"ai.json"
        
        if json_file_name in files:
            json_file_path = os.path.join(subdir, json_file_name)
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                # combined_data.append(data)
                if isinstance(data, list):
                    combined_data.extend(data)
                else:
                    print(f"Warning: {json_file_path} does not contain a JSON array.")

    with open(output_file, 'w') as output_json_file:
        json.dump(combined_data, output_json_file, indent=4)

root_directory = 'actions_lib/actions'
output_json = 'actions_lib/actions/ai.json'
combine_json_files(root_directory, output_json)