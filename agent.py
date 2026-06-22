import anthropic
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone, timedelta

# --- CONFIG ---
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

almaty_tz = timezone(timedelta(hours=5))
today = datetime.now(almaty_tz).strftime("%d %B %Y")
today_ru = datetime.now(almaty_tz).strftime("%d.%m.%Y")


def get_region_news(region_name, region_desc):
    """Fetch news for a single region with one web search."""
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""Today is {today} (Almaty time, UTC+5).

Search the web for today's viral and unusual news from {region_desc}.

You are curating content for Instagram/Reels creators. Include ONLY stories that are:
- 🎭 Genuinely viral, surprising, or heartwarming
- 🏆 Sports records or unexpected wins
- 🔬 Cool tech that visibly changes everyday life
- ✨ Unusual, funny, or culturally fascinating human stories

QUALITY RULE: Only include a story if it truly stands out. If you find 1 strong story — write 1. If you find 3 — write 3. If nothing qualifies today — say so honestly. Never pad the list with weak stories just to fill space. Maximum 5 stories.

STRICTLY EXCLUDE: politics, elections, government, economy, finance, business deals, wars, conflicts, diplomacy, sanctions, GDP, inflation, stock markets.

Format EXACTLY like this:

==={region_name}===
1. [HEADLINE IN ENGLISH]
[1-2 sentence summary in English]

[ЗАГОЛОВОК НА РУССКОМ]
[1-2 предложения на русском]

2. [next story if exists...]

===END===

If nothing qualifies today, write ONLY:
==={region_name}===
No standout stories today.
Достойных историй сегодня нет.
===END===

Start directly with ==={region_name}===. No preamble."""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1500,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 3
        }],
        messages=[{"role": "user", "content": prompt}]
    )

    result = ""
    for block in response.content:
        if block.type == "text":
            result += block.text

    return result


def parse_region(raw, region_name):
    """Extract content for a region from raw response."""
    lines = raw.splitlines()
    content = []
    inside = False

    for line in lines:
        if line.strip() == f"==={region_name}===":
            inside = True
            continue
        elif line.strip() == "===END===":
            inside = False
            break
        elif inside:
            content.append(line)

    return "\n".join(content).strip()


def build_email(china, india, mena):
    body = f"""MORNING PRESS REVIEW | УТРЕННИЙ ОБЗОР ПРЕССЫ
{today} | {today_ru}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🇨🇳 CHINA | КИТАЙ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{china}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🇮🇳 INDIA | ИНДИЯ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{india}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌍 MENA (Middle East & North Africa) | БЛИЖНИЙ ВОСТОК И СЕВЕРНАЯ АФРИКА
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{mena}


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated automatically | Сформировано автоматически
Morning Press Review Agent · Almaty UTC+5 · Mon/Wed/Fri
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

    print("  → China...")
    raw_china = get_region_news("CHINA", "China")
    china = parse_region(raw_china, "CHINA")

    print("  → India...")
    raw_india = get_region_news("INDIA", "India")
    india = parse_region(raw_india, "INDIA")

    print("  → MENA...")
    raw_mena = get_region_news("MENA", "the Middle East and North Africa (MENA region)")
    mena = parse_region(raw_mena, "MENA")

    print("✉️  Building email...")
    body = build_email(china, india, mena)

    print("📤 Sending...")
    send_email(body)
    print("✅ Done!")
