# Weekly Report Emailer

Scrape a job board with requests and BeautifulSoup, then email yourself weekly job alerts.

## Project Structure

```text
├── main.py          # Entry point - orchestrates scrape → email
├── scraper.py       # requests + BeautifulSoup logic
├── emailer.py       # smtplib email sending
├── config.py        # Configuration settings
├── requirements.txt # Python dependencies
├── .env.example     # Template for environment variables
└── sent_jobs.json   # Tracks sent jobs (auto-generated)
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

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

### 3. Gmail App Password Setup

For Gmail, you need an App Password (not your regular password):

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and your device
3. Copy the 16-character password to your `.env` file

### 4. Customize the Scraper

Edit `scraper.py` to match your target job board's HTML structure. Update the CSS selectors in `parse_jobs()`:

```python
job_cards = soup.select(".job-card")  # Update this selector
title_elem = card.select_one(".job-title")  # Update for your site
```

## Usage

### Run Manually

```bash
python main.py
```

### Schedule Weekly (Cron - macOS/Linux)

```bash
# Edit crontab
crontab -e

# Add this line (runs every Monday at 9am)
0 9 * * 1 cd /path/to/project && /usr/bin/python3 main.py >> cron.log 2>&1
```

### Schedule Weekly (Windows Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task → Weekly trigger
3. Action: Start a program → `python` with argument `C:\path\to\main.py`

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
