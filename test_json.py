import json
import re

files = ['static/json/candidate.json', 'static/json/running_mate.json']
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            json.load(file)
            print(f"{f} is OK")
    except Exception as e:
        print(f"Error in {f}: {e}")

try:
    content = open('static/questionset/2020_Biden_Harris.html', 'r', encoding='utf-8').read()
    m = re.search(r'campaignTrail_temp\.questions_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
    if m:
        s = m.group(1).replace('\\"', '"').replace('\\\\', '\\')
        json.loads(s)
        print("questions_json OK")
except Exception as e:
    print(f"Error in questions_json: {e}")
    
try:
    content = open('static/questionset/2020_Biden_Harris.html', 'r', encoding='utf-8').read()
    m = re.search(r'campaignTrail_temp\.answers_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
    if m:
        s = m.group(1).replace('\\"', '"').replace('\\\\', '\\')
        json.loads(s)
        print("answers_json OK")
except Exception as e:
    print(f"Error in answers_json: {e}")
