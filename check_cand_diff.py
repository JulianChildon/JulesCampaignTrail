import json

with open('orig_cand.json', 'r', encoding='utf-8') as f:
    orig = json.load(f)

with open('2020_translated_full.json', 'r', encoding='utf-8') as f:
    trans = json.load(f)
    
with open('static/json/candidate.json', 'r', encoding='utf-8') as f:
    modified = json.load(f)

def check_keys(c):
    keys = list(c['fields'].keys())
    print("Keys in", c['pk'], ":", keys)

for c in orig:
    if str(c['pk']) == '300':
        print("ORIGINAL:")
        print(c['pk'], type(c['pk']))
        check_keys(c)
        break

for c in modified:
    if str(c['pk']) == '300':
        print("MODIFIED:")
        print(c['pk'], type(c['pk']))
        check_keys(c)
        break
