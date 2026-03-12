import json
import re

# We will read campaign_trail.js to see where candidates are loaded.
with open('static/js/campaign_trail.js', 'r', encoding='utf-8') as f:
    ct = f.read()

# Is there anything wrong with candidate.json?
with open('static/json/candidate.json', 'r', encoding='utf-8') as f:
    cands = json.load(f)

# Are there any newlines or unescaped quotes in the descriptions?
for c in cands:
    if str(c['pk']) == '300':
        print("Biden desc:", repr(c['fields']['description']))

with open('static/questionset/2020_Biden_Harris.html', 'r', encoding='utf-8') as f:
    html = f.read()
    
# Let's extract the exact string that is parsed in the html for Biden 2020
m = re.search(r'campaignTrail_temp\.questions_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', html)
if m:
    s = m.group(1)
    if '\\"' not in s and '"' in s:
        print("Warning: unescaped quotes in questions_json JS string!")
    else:
        print("questions_json js string looks okay.")
        
m = re.search(r'campaignTrail_temp\.answers_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', html)
if m:
    s = m.group(1)
    if '\\"' not in s and '"' in s:
        print("Warning: unescaped quotes in answers_json JS string!")
    else:
        print("answers_json js string looks okay.")
