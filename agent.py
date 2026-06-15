import anthropic
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- CONFIG ---
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

# Almaty is UTC+5
from datetime import timezone, timedelta
almaty_tz = timezone(timedelta(hours=5))
today = datetime.now(almaty_tz).strftime("%d %B %Y")
today_ru = datetime.now(almaty_tz).strftime("%d.%m.%Y")


def get_digest():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""Today is {today} (Almaty time, UTC+5).

You are a senior analyst preparing a morning press digest for an executive. 

Search the web for today's most significant news from THREE regions:
1. China
2. India  
3. MENA (Middle East & North Africa)

Focus ONLY on these two categories:
- 🔬 Technology & Innovation (AI, startups, launches, breakthroughs, policy)
- 🎭 Culture, Sports & Society (major events, records, notable figures, social trends)

For each region, select UP TO 5 most resonant events. "Resonant" means:
- Wide impact (national, regional or global scale)
- Surprising or groundbreaking
- Relevant to current trends

Format your response EXACTLY like this (keep the structure, use the exact separators):

===CHINA===
1. [HEADLINE IN ENGLISH]
[1-2 sentence summary in English]

[ЗАГОЛОВОК НА РУССКОМ]
[1-2 предложения на русском]

2. [next event...]

===INDIA===
[same structure]

===MENA===
[same structure]

===END===

If no resonant events found for a region, write:
No major resonant events found today.
Значимых событий за сегодня не найдено.

Be concise. No preamble. Start directly with ===CHINA==="""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract text from response
    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text

    return result


def parse_digest(raw):
    """Parse the structured digest into sections."""
    sections = {"CHINA": "", "INDIA": "", "MENA": ""}
    current = None

    for line in raw.splitlines():
        if line.strip() == "===CHINA===":
            current = "CHINA"
        elif line.strip() == "===INDIA===":
            current = "INDIA"
        elif line.strip() == "===MENA===":
            current = "MENA"
        elif line.strip() == "===END===":
            current = None
        elif current:
            sections[current] += line + "\n"

    return sections


def build_email(sections):
    body = f"""MORNING PRESS REVIEW | УТРЕННИЙ ОБЗОР ПРЕССЫ
{today} | {today_ru}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🇨🇳 CHINA | КИТАЙ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{sections["CHINA"].strip()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🇮🇳 INDIA | ИНДИЯ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{sections["INDIA"].strip()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 MENA (Middle East & North Africa) | БЛИЖНИЙ ВОСТОК И СЕВЕРНАЯ АФРИКА
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{sections["MENA"].strip()}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated automatically | Сформировано автоматически
Morning Press Review Agent · Almaty UTC+5
"""
    return body


def send_email(body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🌏 Morning Press Review — {today} | Утренний обзор прессы"
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT_EMAIL

    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, msg.as_string())

    print(f"✅ Email sent to {RECIPIENT_EMAIL}")


if __name__ == "__main__":
    print(f"🔍 Fetching news for {today}...")
    raw = get_digest()
    print("📋 Parsing digest...")
    sections = parse_digest(raw)
    print("✉️  Building email...")
    body = build_email(sections)
    print("📤 Sending...")
    send_email(body)
    print("✅ Done!")
