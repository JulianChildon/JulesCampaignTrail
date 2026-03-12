import json
import re
import os

html_file = 'static/questionset/2020_Biden_Harris.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's check how the JSON looks
for var in ['questions_json', 'answers_json', 'states_json', 'issue_score_json', 'state_issue_score_json']:
    m = re.search(fr'campaignTrail_temp\.{var}\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
    if m:
        try:
            s = m.group(1)
            # Find any non-escaped inner quotes?
            s2 = s.replace('\\"', '"').replace('\\\\', '\\')
            
            # test parse
            j = json.loads(s2)
            print(f"{var}: OK ({len(j)} items)")
        except Exception as e:
            print(f"{var}: Error parsing - {e}")
            print("Preview:", s[:100])
    
# Let's check if there are raw newlines in the match, which would break JS literal
m = re.search(r'campaignTrail_temp\.questions_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
if m:
    if '\n' in m.group(1):
        print("questions_json contains literal newlines!")
    if '\r' in m.group(1):
        print("questions_json contains literal carriage returns!")

m = re.search(r'campaignTrail_temp\.answers_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
if m:
    if '\n' in m.group(1):
        print("answers_json contains literal newlines!")
    if '\r' in m.group(1):
        print("answers_json contains literal carriage returns!")
