import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Use Gmail App Password
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", EMAIL_ADDRESS)

# SMTP Settings (Gmail defaults)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Job Board Configuration
JOB_BOARD_URL = os.getenv("JOB_BOARD_URL", "https://sfbay.craigslist.org/search/jjj")
SEARCH_KEYWORDS = ["python", "remote", "frontend", "front-end", "web developer"]

# File to track sent jobs (avoid duplicates)
SENT_JOBS_FILE = "sent_jobs.json"

# Request settings
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 2  # seconds between requests
