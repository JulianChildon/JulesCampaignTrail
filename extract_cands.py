import json

with open("static/json/candidate.json", "r", encoding="utf-8") as f:
    cands = json.load(f)

with open("static/json/running_mate.json", "r", encoding="utf-8") as f:
    rms = json.load(f)

with open("2020_to_translate.json", "r", encoding="utf-8") as f:
    trans = json.load(f)

# election 21 is 2020
for c in cands:
    if c['fields'].get('election') == 21:
        pk = str(c["pk"])
        trans["candidates"][pk] = {
            "first_name": c["fields"]["first_name"],
            "last_name": c["fields"]["last_name"],
            "description": c["fields"]["description"],
            "electoral_victory_message": c["fields"]["electoral_victory_message"],
            "electoral_loss_message": c["fields"]["electoral_loss_message"],
            "no_electoral_majority_message": c["fields"]["electoral_loss_message"], # usually same or similar
        }

# wait, running mates don't have 'election'. They have 'candidate' which refers to the presidential candidate pk.
biden_pk = 300
trump_pk = 301
for rm in rms:
    fields = rm["fields"]
    cand_ref = fields.get("candidate")
    if cand_ref in [biden_pk, trump_pk]:
        pk = str(rm["pk"])
        trans["running_mates"][pk] = {
            "first_name": fields.get("first_name", ""),
            "last_name": fields.get("last_name", ""),
            "description_as_running_mate": fields.get("description_as_running_mate", "")
        }

with open("2020_to_translate.json", "w", encoding="utf-8") as f:
    json.dump(trans, f, indent=2, ensure_ascii=False)

print(f"Added {len(trans['candidates'])} candidates and {len(trans['running_mates'])} running mates.")
