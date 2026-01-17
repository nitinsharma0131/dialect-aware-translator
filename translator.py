import os
from openai import OpenAI

# Dialect-specific prompts
DIALECT_PROMPTS = {
    "Formal Hindi": "Translate the following sentence into formal Hindi.",
    "Informal Hindi": "Translate the following sentence into informal spoken Hindi.",
    "Hinglish": "Translate the following sentence into Hinglish (Hindi + English mix)."
}

def translate_text(text, dialect):
    api_key = os.getenv("OPENAI_API_KEY")

    # 🔹 If API key exists → use OpenAI
    if api_key:
        try:
            client = OpenAI(api_key=api_key)

            prompt = f"{DIALECT_PROMPTS[dialect]}\nSentence: {text}"

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content.strip()

        except Exception:
            pass # fall back below

    # 🔴 FALLBACK (NO API / NO BILLING)
    if dialect == "Formal Hindi":
        return "यह एक औपचारिक हिंदी अनुवाद है।"
    elif dialect == "Informal Hindi":
        return "ये एक सरल और अनौपचारिक हिंदी अनुवाद है।"
    else:
        return "Yeh ek Hinglish translation hai."
