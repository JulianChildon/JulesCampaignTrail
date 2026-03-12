import json

def check_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {os.path.basename(file_path)} with {len(data)} items.")
    return data

import os
cands = check_json('static/json/candidate.json')
rms = check_json('static/json/running_mate.json')

# Check if there are any missing keys that JS expects
for c in cands:
    if str(c['pk']) == '300':
        assert 'first_name' in c['fields']
        assert 'last_name' in c['fields']
        assert 'description' in c['fields']
        assert 'electoral_victory_message' in c['fields']
        assert 'electoral_loss_message' in c['fields']
        assert 'no_electoral_majority_message' in c['fields']

print("All expected keys present in candidates.")
