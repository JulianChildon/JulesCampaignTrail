import os
import json
import re

HTML_DIR = "static/questionset"
OUTPUT_FILE = "2020_to_translate.json"

FILES = [
    f for f in os.listdir(HTML_DIR)
    if f.startswith("2020_") and f.endswith(".html")
]

# We need to extract:
# 1. candidate_json: description, electoral_*_messages
# 2. running_mate_json: description_as_running_mate
# 3. questions_json: description
# 4. answers_json: description
# 5. The intro text in the HTML (like "What will you say to the American people...")?
# Actually, the questions_json has the description (which is the question prompt).
# The introductory text inside the html `<div class="inner_inner_window"><h3>What will you say...</h3>` 
# is hardcoded in SOME files, but mostly it's dynamic based on the JSON. Wait, in 2020_Biden_Harris.html line 2, there is hardcoded text for the very first question?
# Actually, the first question's text might be hardcoded as a placeholder. We should check if we need to translate the raw HTML too. 

def extract_strings():
    translations = {
        "candidates": {},
        "running_mates": {},
        "questions": {},
        "answers": {},
        "endings": {},
        "raw_html": {}
    }
    
    for filename in FILES:
        filepath = os.path.join(HTML_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse candidate
        cand_match = re.search(r'campaignTrail_temp\.candidate_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
        if cand_match:
            try:
                # The JSON.parse string is usually doubly-escaped or just a raw string. 
                # Let's use json.loads directly if possible, but we need to unescape backslashes.
                raw_json = cand_match.group(1).replace('\\"', '"').replace('\\\\', '\\')
                cands = json.loads(f'[{raw_json}]') if not raw_json.startswith('[') else json.loads(raw_json)
                for c in cands:
                    if isinstance(c, dict) and "fields" in c:
                        pk = str(c["pk"])
                        fields = c["fields"]
                        translations["candidates"][pk] = {
                            "first_name": fields.get("first_name", ""),
                            "last_name": fields.get("last_name", ""),
                            "description": fields.get("description", ""),
                            "electoral_victory_message": fields.get("electoral_victory_message", ""),
                            "electoral_loss_message": fields.get("electoral_loss_message", ""),
                            "no_electoral_majority_message": fields.get("no_electoral_majority_message", "")
                        }
            except Exception as e:
                print(f"Error parsing candidate in {filename}: {e}")

        # running mate
        rm_match = re.search(r'campaignTrail_temp\.running_mate_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
        if rm_match:
            try:
                raw_json = rm_match.group(1).replace('\\"', '"').replace('\\\\', '\\')
                rms = json.loads(f'[{raw_json}]') if not raw_json.startswith('[') else json.loads(raw_json)
                for rm in rms:
                    if isinstance(rm, dict) and "fields" in rm:
                        pk = str(rm["pk"])
                        fields = rm["fields"]
                        translations["running_mates"][pk] = {
                            "first_name": fields.get("first_name", ""),
                            "last_name": fields.get("last_name", ""),
                            "description_as_running_mate": fields.get("description_as_running_mate", "")
                        }
            except Exception as e:
                print(f"Error parsing running_mate in {filename}: {e}")

        # questions
        q_match = re.search(r'campaignTrail_temp\.questions_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
        if q_match:
            try:
                raw_json = q_match.group(1).replace('\\"', '"').replace('\\\\', '\\')
                qs = json.loads(raw_json)
                for q in qs:
                    if isinstance(q, dict) and "fields" in q:
                        pk = str(q["pk"])
                        translations["questions"][pk] = q["fields"].get("description", "")
            except Exception as e:
                print(f"Error parsing questions in {filename}: {e}")
                
        # answers
        a_match = re.search(r'campaignTrail_temp\.answers_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', content)
        if a_match:
            try:
                raw_json = a_match.group(1).replace('\\"', '"').replace('\\\\', '\\')
                ans = json.loads(raw_json)
                for a in ans:
                    if isinstance(a, dict) and "fields" in a:
                        pk = str(a["pk"])
                        translations["answers"][pk] = a["fields"].get("description", "")
            except Exception as e:
                print(f"Error parsing answers in {filename}: {e}")

        # Check for hardcoded raw html intro text, like the first question 
        html_q = re.search(r'<h3>(.*?)</h3>', content.split('<script>')[0])
        if html_q:
            translations["raw_html"]["intro_h3"] = html_q.group(1)
            
        # extract any JS hardcoded strings from endingPicker
        js_endings = re.findall(r'(?:extramessagemargin|titlemessage|lostmarginmessage|return)\s*=\s*"(.*?)"', content)
        # Also let's just grab the whole JS ending message logic? It's too complex. 
        # I'll manually translate the endingPicker strings later using multi_replace_file_content since they are shared across files!
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(translations, f, indent=2, ensure_ascii=False)
        
    print(f"Extracted API data to {OUTPUT_FILE}")
    print(f"Unique questions: {len(translations['questions'])}")
    print(f"Unique answers: {len(translations['answers'])}")
    print(f"Unique candidates: {len(translations['candidates'])}")
    print(f"Unique running mates: {len(translations['running_mates'])}")

if __name__ == "__main__":
    extract_strings()
