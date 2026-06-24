[README (1).md](https://github.com/user-attachments/files/29280895/README.1.md)
# 🌏 Morning Press Review Agent

Automated morning news digest covering China, India, and MENA.
Delivered every **Monday, Wednesday, and Friday at 8:00 AM Almaty time (UTC+5)**.

## What It Does

Searches the web for viral and lifestyle news from three regions and sends a bilingual
Russian/English email digest focused on content that inspires Instagram and Reels creators.

**Content categories:**
- 🎭 Viral moments, celebrity news, fashion, food trends, travel, beauty
- 🏆 Sports achievements, records, unexpected wins
- 🔬 Cool tech that changes everyday life
- ✨ Unusual, funny, or heartwarming human stories

**Strictly excluded:** politics, elections, economy, finance, wars, conflicts, diplomacy.

## How It Works

1. Runs automatically on Mon/Wed/Fri at 3:00 AM UTC (8:00 AM Almaty)
2. Makes 3 separate API calls — one per region (China, India, MENA)
3. Each call uses up to 3 web searches with quality threshold filtering
4. Sends a single bilingual email with all regions

## Setup (one time only)

### 1. Get Gmail App Password
Regular Gmail password won't work — you need an App Password.
1. Go to **myaccount.google.com/security**
2. Enable **2-Step Verification** if not already on
3. Search for **"App Passwords"**
4. Create new → name it "Morning Digest"
5. Copy the 16-character code (shown only once)

### 2. Add GitHub Secrets
Repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Your key from console.anthropic.com |
| `GMAIL_USER` | Sender Gmail address |
| `GMAIL_APP_PASSWORD` | 16-character app password from step 1 |
| `RECIPIENT_EMAIL` | Email address to receive the digest |

### 3. Fund the Anthropic API
Go to **console.anthropic.com** → **Billing** → add $5 credits.
At current usage (~$0.05/run × 12 runs/month) — $5 lasts approximately 8 months.

### 4. Test manually
Repository → **Actions** → **Morning Press Review** → **Run workflow**
If email arrives — everything works. The agent will run automatically from here.

## Repository Structure

```
morning-press-review/
├── agent.py                      # Main agent script
├── .github/
│   └── workflows/
│       └── daily-digest.yml      # Schedule and workflow config
└── README.md
```

## Cost

| Parameter | Value |
|---|---|
| Model | claude-haiku-4-5 |
| Web searches per run | max 9 (3 per region) |
| Cost per run | ~$0.03–0.05 |
| Monthly cost (Mon/Wed/Fri) | ~$0.60 |
