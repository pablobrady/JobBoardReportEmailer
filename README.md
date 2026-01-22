# Weekly Report Emailer

Scrape a job board with requests and BeautifulSoup, then email yourself weekly job alerts.

## Project Structure

```text
├── main.py          # Entry point - orchestrates scrape → email
├── scraper.py       # requests + BeautifulSoup logic
├── emailer.py       # smtplib email sending
├── config.py        # Configuration settings
├── pyproject.toml   # Project dependencies (uv)
├── .env.example     # Template for environment variables
└── sent_jobs.json   # Tracks sent jobs (auto-generated)
```

## Setup (macOS)

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```bash
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=your_email@gmail.com
JOB_BOARD_URL=https://your-target-jobboard.com/jobs
```

### 4. Gmail App Password Setup

For Gmail, you need an App Password (not your regular password):

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and your device
3. Copy the 16-character password to your `.env` file

### 5. Customize the Scraper

Edit `scraper.py` to match your target job board's HTML structure. Update the CSS selectors in `parse_jobs()`:

```python
job_cards = soup.select(".job-card")  # Update this selector
title_elem = card.select_one(".job-title")  # Update for your site
```

## Usage

### Run Manually

```bash
uv run python main.py
```

### Schedule Weekly (macOS launchd)

launchd is the recommended way to schedule tasks on macOS.

**Install the plist:**

```bash
mkdir -p ~/Library/LaunchAgents
cp com.jobemailer.weekly.plist ~/Library/LaunchAgents/
```

Edit `~/Library/LaunchAgents/com.jobemailer.weekly.plist` and update the path to your project directory.

**Load the schedule:**

```bash
launchctl load ~/Library/LaunchAgents/com.jobemailer.weekly.plist
```

**Unload/stop:**

```bash
launchctl unload ~/Library/LaunchAgents/com.jobemailer.weekly.plist
```

**Test immediately:**

```bash
launchctl start com.jobemailer.weekly
```

## Configuration

Edit `config.py` to customize:

- `SEARCH_KEYWORDS` - Filter jobs by keywords in title
- `REQUEST_DELAY` - Seconds between requests (be respectful)
- `SMTP_SERVER/PORT` - Change for non-Gmail providers

## Key Features

- Deduplication: Tracks sent jobs in `sent_jobs.json` to avoid repeats
- Keyword filtering: Only sends jobs matching your search terms
- HTML + Plain text emails: Works in all email clients
- Rate limiting: Configurable delays between requests

---

## AI-Builders Assignment #1

> Build your own custom automation using only Software 1.0 (no AI API calls).

**Selected Project:** Weekly Report Emailer
