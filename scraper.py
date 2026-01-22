import time
import json
import requests
from bs4 import BeautifulSoup
from config import (
    JOB_BOARD_URL,
    SEARCH_KEYWORDS,
    SENT_JOBS_FILE,
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
)


def load_sent_jobs():
    """Load previously sent job IDs to avoid duplicates."""
    try:
        with open(SENT_JOBS_FILE, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def save_sent_jobs(job_ids):
    """Save job IDs that have been sent."""
    with open(SENT_JOBS_FILE, "w") as f:
        json.dump(list(job_ids), f)


def fetch_page(url):
    """Fetch a page and return BeautifulSoup object."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def parse_jobs(soup):
    """
    Parse job listings from the page.
    Configured for Craigslist structure.
    """
    jobs = []

    # Craigslist selectors
    job_cards = soup.select("li.cl-static-search-result")

    for card in job_cards:
        try:
            title_elem = card.select_one(".title")
            location_elem = card.select_one(".location")
            price_elem = card.select_one(".price")
            link_elem = card.select_one("a[href]")

            job = {
                "title": title_elem.get_text(strip=True) if title_elem else "Unknown",
                "company": price_elem.get_text(strip=True) if price_elem else "",
                "location": location_elem.get_text(strip=True) if location_elem else "Unknown",
                "url": link_elem.get("href", "") if link_elem else "",
                "id": None,
            }

            # Create unique ID from URL (most reliable for Craigslist)
            if job["url"]:
                job["id"] = job["url"].split("/")[-1].replace(".html", "")
            else:
                job["id"] = f"{job['title']}_{job['location']}".lower().replace(" ", "_")
            jobs.append(job)

        except Exception as e:
            print(f"Error parsing job card: {e}")
            continue

    return jobs


def filter_jobs(jobs, keywords):
    """Filter jobs by keywords in title."""
    if not keywords:
        return jobs

    filtered = []
    for job in jobs:
        title_lower = job["title"].lower()
        if any(kw.lower() in title_lower for kw in keywords):
            filtered.append(job)
    return filtered


def scrape_jobs():
    """Main scraping function. Returns list of new jobs."""
    print(f"Scraping jobs from: {JOB_BOARD_URL}")

    sent_jobs = load_sent_jobs()

    try:
        soup = fetch_page(JOB_BOARD_URL)
        time.sleep(REQUEST_DELAY)  # Be respectful

        all_jobs = parse_jobs(soup)
        print(f"Found {len(all_jobs)} total jobs")

        # Filter by keywords
        filtered_jobs = filter_jobs(all_jobs, SEARCH_KEYWORDS)
        print(f"Found {len(filtered_jobs)} jobs matching keywords: {SEARCH_KEYWORDS}")

        # Remove already-sent jobs
        new_jobs = [j for j in filtered_jobs if j["id"] not in sent_jobs]
        print(f"Found {len(new_jobs)} new jobs")

        # Update sent jobs tracker
        if new_jobs:
            sent_jobs.update(j["id"] for j in new_jobs)
            save_sent_jobs(sent_jobs)

        return new_jobs

    except requests.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return []


if __name__ == "__main__":
    # Test the scraper
    jobs = scrape_jobs()
    for job in jobs:
        print(f"- {job['title']} at {job['company']} ({job['location']})")
