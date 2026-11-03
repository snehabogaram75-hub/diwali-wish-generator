import csv, os, random
from concurrent.futures import ThreadPoolExecutor
from wish import client, generate_wish, TONE

NAMES = ["Ravi", "Sneha", "Kiran", "Priya", "Suresh", "Anil", "Lakshmi", "Venkat", "Divya", "Harsha", "Meena", "Karthik"]
LANGS = ["Tanglish", "Tanglish", "Tanglish", "English", "Telugu", "Hindi"]
FILE = "labels.csv"
FIELDS = ["name", "relation", "language", "source", "wish", "label"]

def poetic(name, relation, language):
    prompt = f"Write a beautiful, poetic Diwali greeting for {name}, my {relation}, in {language}. 2-3 sentences with emojis. Return only the greeting."
    r = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0, max_tokens=1000, reasoning_effort="low",
    )
    return r.choices[0].message.content.strip()

def make_one(_):
    name, rel, lang = random.choice(NAMES), random.choice(list(TONE)), random.choice(LANGS)
    src = random.choice(["tuned", "poetic"])
    try:
        text = generate_wish(name, rel, lang) if src == "tuned" else poetic(name, rel, lang)
    except Exception:
        return None
    return {"name": name, "relation": rel, "language": lang, "source": src, "wish": text}

existing = 0
if os.path.exists(FILE):
    existing = sum(1 for _ in open(FILE, encoding="utf-8")) - 1
n = existing
print(f"Labels so far: {existing}. Target: 100. Label 1 = natural, 0 = stiff (too poetic/formal/cliche or wrong tone for the relation).")

with open(FILE, "a", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    if existing <= 0:
        w.writeheader()
    while True:
        with ThreadPoolExecutor(3) as ex:
            batch = [b for b in ex.map(make_one, range(9)) if b]
        for b in batch:
            print(f"\n[{n + 1}] {b['relation']} | {b['language']}\n{b['wish']}")
            while True:
                a = input("natural=1  stiff=0  skip=s  quit=q > ").strip().lower()
                if a in ("1", "0", "s", "q"):
                    break
            if a == "q":
                print(f"Saved. Total labels: {n}")
                raise SystemExit
            if a == "s":
                continue
            b["label"] = a
            w.writerow(b)
            f.flush()
            n += 1
