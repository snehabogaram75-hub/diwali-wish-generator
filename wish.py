import os
from groq import Groq

def load_key():
    if os.path.exists(".env"):
        for line in open(".env"):
            if line.startswith("GROQ_API_KEY="):
                return line.strip().split("=", 1)[1]
    return os.getenv("GROQ_API_KEY")

client = Groq(api_key=load_key())

TONE = {
    "friend": "casual, playful, teasing, like texting a close friend (use 'ra'/'macha')",
    "brother": "casual, playful, brotherly",
    "sister": "warm, affectionate, a little playful",
    "amma": "loving, respectful, emotional but simple",
    "nanna": "loving, respectful, simple",
    "boss": "polite, formal, professional, no slang",
    "colleague": "friendly but professional",
    "teacher": "respectful, grateful, formal",
    "student": "encouraging, warm, like a tutor wishing a student",
    "relative": "warm, respectful, family-like",
}

EXAMPLES = """Examples of the style (do NOT copy them, just match the naturalness):
Tanglish friend: Ey Ravi! Happy Diwali ra 🪔 Ee roju sweets tinu, crackers kalchu, full enjoy cheyyi. Party ekkada ra?
Tanglish amma: Amma, Happy Diwali! 🪔 Nuvvu unte maa intlo prathi roju deepavali ne. Love you amma!
English boss: Wishing you and your family a very Happy Diwali. May the year ahead bring you success and good health."""

def generate_wish(name, relation, language="Tanglish"):
    tone = TONE.get(relation, "warm and natural")
    prompt = f"""Write a Diwali wish for {name}, who is my {relation}.
Language: {language}. (Tanglish = Telugu in English letters mixed with English, the way Telugu people actually text on WhatsApp.)
Tone: {tone}.

Rules:
- Exactly 2 short sentences. Max 35 words.
- Sound like a real person texting, NOT a poem or greeting card.
- No flowery or bookish words, no clichés like "light up your life" or "sparkle".
- Use {name}'s name once. Use 1-2 emojis (🪔 ✨ 🎆 🎇).
- If Language is Telugu, write in Telugu script (తెలుగు) only. For every other language use Roman letters only, never Tamil, Telugu or Devanagari script.

{EXAMPLES}

Return only the wish text."""
    r = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        max_tokens=1000,
        reasoning_effort="low",
    )
    return r.choices[0].message.content.strip()

if __name__ == "__main__":
    print(generate_wish("Ravi", "friend", "Tanglish"))
    print(generate_wish("Amma", "amma", "Tanglish"))
    print(generate_wish("Suresh", "boss", "English"))
