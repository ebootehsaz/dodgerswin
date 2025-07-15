# Dodgers Panda Express Coupon Checker

This GitHub Actions automation checks if the Los Angeles Dodgers won a home game yesterday, which means the Panda Express `DODGERSWIN` coupon is likely active today. If so, it sends an alert to a Discord channel via webhook.

---

## Features

- Checks the MLB Stats API daily at 6 AM PT
- Sends a Discord alert only if the Dodgers won a home game
- Uses a simple Discord Webhook (no bot token or hosting required)
- Includes a debug mode for local testing
- Runs entirely via GitHub Actions (no server or manual cron setup needed)

---

## How It Works

1. The script (`checker.py`) queries the MLB Stats API for the Dodgers’ game from the previous day.
2. If the Dodgers:
   - Played at home, and
   - Won the game
3. A message is posted to your configured Discord webhook stating the coupon is likely active.

---

## Setup Instructions

### 1. Create a Discord Webhook

1. Open your Discord server and navigate to the desired channel.
2. Go to Settings → Integrations → Webhooks → New Webhook.
3. Name the webhook (e.g., "Dodgers Coupon Bot") and copy the Webhook URL.

### 2. Add the Webhook to GitHub Secrets

1. In your GitHub repository, go to: Settings → Secrets and variables → Actions.
2. Click “New repository secret”.
3. Set the name to `DISCORD_WEBHOOK_URL`.
4. Paste in your Discord Webhook URL.

### 3. File Structure

```
.
├── check_coupon.py
└── .github/
    └── workflows/
        └── check.yml
```

---

## GitHub Actions Workflow

The workflow is scheduled to run automatically every day at 6:00 AM Pacific Time:

```yaml
on:
  schedule:
    - cron: '0 13 * * *'  # 6 AM PT
  workflow_dispatch:        # Enables manual execution from the GitHub UI
```

You can also manually run the workflow from the GitHub Actions tab.

---

## Local Debug Mode

In `check_coupon.py`, set:

```python
DEBUG = 1
```

This will:
- Print internal information to the console
- Always send a message to the webhook, regardless of outcome
- Use a hardcoded webhook instead of reading from secrets

Set `DEBUG = 0` to disable verbose output and restrict alerts to only valid coupon conditions.

---

## Requirements

Only one external Python dependency is required:

```bash
pip install requests
```

---

## Example Output

If conditions are met:

```
Dodgers won at home on 2025-07-13. Coupon likely active today.
```

---
