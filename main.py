#!/usr/bin/env python3
"""
Weekly Job Report Emailer

Scrapes job listings and sends weekly email alerts.
Run manually or schedule with cron/Task Scheduler.
"""

from scraper import scrape_jobs
from emailer import send_email


def main():
    print("=" * 50)
    print("Weekly Job Report Emailer")
    print("=" * 50)

    # Scrape new jobs
    jobs = scrape_jobs()

    if not jobs:
        print("No new jobs to report.")
        return

    # Send email
    print(f"\nSending email with {len(jobs)} job(s)...")
    success = send_email(jobs)

    if success:
        print("\nJob report sent successfully!")
    else:
        print("\nFailed to send job report.")


if __name__ == "__main__":
    main()
