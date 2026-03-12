import json
import codecs

def restore_cands():
    # Read the original files using utf-8-sig to handle optional BOM
    with open('static/json/candidate.json', 'r', encoding='utf-8-sig') as f:
        cands = json.load(f)
    with open('static/json/running_mate.json', 'r', encoding='utf-8-sig') as f:
        rms = json.load(f)
        
    with open('2020_translated_full.json', 'r', encoding='utf-8') as f:
        trans = json.load(f)
        
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

    # Write back ensuring ascii so pure unicode \uXXXX is used
    with open("static/json/candidate.json", "w", encoding='utf-8') as f:
        json.dump(cands, f, indent=2, ensure_ascii=True)
        
    with open("static/json/running_mate.json", "w", encoding='utf-8') as f:
        json.dump(rms, f, indent=2, ensure_ascii=True)
        
    print(f"Re-injected candidates ({count_c}) and running mates ({count_r}) with ensure_ascii=True")

restore_cands()
