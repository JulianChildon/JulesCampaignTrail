import json
import os
import re

def main():
    with open("2020_translated_cands.json", "r", encoding="utf-8") as f:
        cands = json.load(f)
    with open("2020_translated_questions.json", "r", encoding="utf-8") as f:
        qs = json.load(f)
    with open("2020_translated_answers1.json", "r", encoding="utf-8") as f:
        ans1 = json.load(f)
    with open("2020_translated_answers2.json", "r", encoding="utf-8") as f:
        ans2 = json.load(f)
        
    combined = {
        "candidates": cands.get("candidates", {}),
        "running_mates": cands.get("running_mates", {}),
        "questions": qs.get("questions", {}),
        "answers": ans1
    }
    combined["answers"].update(ans2)

    # Let's also translate the hardcoded raw_html intro text 
    # Original: "What will you say to the American people as you accept your party's nomination for President?"
    combined["raw_html"] = {
        "intro_h3": "当您接受本党总统提名时，您会对美国人民说些什么？"
    }

    with open("2020_translated_full.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
        
    print("Combined JSON saved to 2020_translated_full.json")
    print(f"Cand: {len(combined['candidates'])}, RM: {len(combined['running_mates'])}, Qs: {len(combined['questions'])}, Ans: {len(combined['answers'])}")

if __name__ == "__main__":
    main()
