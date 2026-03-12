import os
import json
import re

TRANS_FILE = "2020_translated_full.json"
HTML_DIR = "static/questionset"

def main():
    with open(TRANS_FILE, "r", encoding="utf-8") as f:
        trans = json.load(f)

    # 1. Update candidate.json
    with open("static/json/candidate.json", "r", encoding="utf-8") as f:
        cands = json.load(f)
    count_c = 0
    for c in cands:
        pk = str(c["pk"])
        if pk in trans["candidates"]:
            t = trans["candidates"][pk]
            if t["first_name"] and t["first_name"] != "'": c["fields"]["first_name"] = t["first_name"]
            if t["last_name"] and t["last_name"] != "'": c["fields"]["last_name"] = t["last_name"]
            if t["description"] and t["description"] != "'":
                c["fields"]["description"] = t["description"]
            if t["electoral_victory_message"] and t["electoral_victory_message"] != "'":
                c["fields"]["electoral_victory_message"] = t["electoral_victory_message"]
            if t["electoral_loss_message"] and t["electoral_loss_message"] != "'":
                c["fields"]["electoral_loss_message"] = t["electoral_loss_message"]
            if t["no_electoral_majority_message"] and t["no_electoral_majority_message"] != "'":
                c["fields"]["no_electoral_majority_message"] = t["no_electoral_majority_message"]
            count_c += 1

    with open("static/json/candidate.json", "w", encoding="utf-8") as f:
        json.dump(cands, f, indent=2, ensure_ascii=False)

    # 2. Update running_mate.json
    with open("static/json/running_mate.json", "r", encoding="utf-8") as f:
        rms = json.load(f)
    count_r = 0
    for rm in rms:
        pk = str(rm["pk"])
        if pk in trans["running_mates"]:
            t = trans["running_mates"][pk]
            if t["first_name"] and t["first_name"] != "'": rm["fields"]["first_name"] = t["first_name"]
            if t["last_name"] and t["last_name"] != "'": rm["fields"]["last_name"] = t["last_name"]
            if t["description_as_running_mate"] and t["description_as_running_mate"] != "'":
                rm["fields"]["description_as_running_mate"] = t["description_as_running_mate"]
            count_r += 1
                
    with open("static/json/running_mate.json", "w", encoding="utf-8") as f:
        json.dump(rms, f, indent=2, ensure_ascii=False)

    # 3. Update HTML files
    html_files = [f for f in os.listdir(HTML_DIR) if f.startswith("2020_") and f.endswith(".html")]
    for filename in html_files:
        filepath = os.path.join(HTML_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace questions
        def repl_q(match):
            raw_json = match.group(1).replace('\\"', '"').replace('\\\\', '\\')
            data = json.loads(raw_json)
            for item in data:
                pk = str(item["pk"])
                if pk in trans["questions"]:
                    item["fields"]["description"] = trans["questions"][pk]
            new_json = json.dumps(data, ensure_ascii=False)
            new_json = new_json.replace('\\', '\\\\').replace('"', '\\"')
            return f'campaignTrail_temp.questions_json = JSON.parse("{new_json}");'
        
        content = re.sub(r'campaignTrail_temp\.questions_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', repl_q, content)

        # Replace answers
        def repl_a(match):
            raw_json = match.group(1).replace('\\"', '"').replace('\\\\', '\\')
            data = json.loads(raw_json)
            for item in data:
                pk = str(item["pk"])
                if pk in trans["answers"]:
                    item["fields"]["description"] = trans["answers"][pk]
            new_json = json.dumps(data, ensure_ascii=False)
            new_json = new_json.replace('\\', '\\\\').replace('"', '\\"')
            return f'campaignTrail_temp.answers_json = JSON.parse("{new_json}");'

        content = re.sub(r'campaignTrail_temp\.answers_json\s*=\s*JSON\.parse\(\"(.*?)\"\);', repl_a, content)

        # Replace raw_html
        content = content.replace(
            "What will you say to the American people as you accept your party's nomination for President?",
            "当您接受本党总统提名时，您会对美国人民说些什么？"
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"Injection complete! Cands: {count_c}, RMs: {count_r}, Files: {len(html_files)}")

if __name__ == "__main__":
    main()
