import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from mjml import mjml_to_html
from config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    RECIPIENT_EMAIL,
    SMTP_SERVER,
    SMTP_PORT,
)

# Purple color scheme
COLORS = {
    "primary": "#7c3aed",      # Purple
    "primary_dark": "#5b21b6", # Darker purple
    "background": "#faf5ff",   # Light purple tint
    "text": "#1f2937",         # Dark gray
    "text_light": "#6b7280",   # Medium gray
    "button": "#8b5cf6",       # Action purple
}


def build_job_cards_mjml(jobs):
    """Build MJML markup for job cards."""
    if not jobs:
        return """
        <mj-section>
          <mj-column>
            <mj-text align="center" color="#6b7280">No new jobs found.</mj-text>
          </mj-column>
        </mj-section>
        """

    cards = ""
    for job in jobs:
        cards += f"""
        <mj-section background-color="#ffffff" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="{COLORS['primary_dark']}">
              {job['title']}
            </mj-text>
            <mj-text color="{COLORS['text_light']}" padding-top="0">
              📍 {job['location']} {f"&nbsp;&nbsp;💰 {job['company']}" if job['company'] else ""}
            </mj-text>
            <mj-button background-color="{COLORS['button']}" href="{job['url']}" border-radius="6px">
              View Job
            </mj-button>
          </mj-column>
        </mj-section>
        <mj-section padding="10px"></mj-section>
        """
    return cards


def build_email_mjml(jobs, date_str):
    """Build complete MJML email template."""
    job_cards = build_job_cards_mjml(jobs)

    template = f"""
    <mjml>
      <mj-head>
        <mj-attributes>
          <mj-all font-family="Arial, sans-serif" />
          <mj-text font-size="14px" line-height="1.5" />
        </mj-attributes>
      </mj-head>
      <mj-body background-color="{COLORS['background']}">
        <!-- Header -->
        <mj-section background-color="{COLORS['primary']}" padding="30px 20px">
          <mj-column>
            <mj-text align="center" color="#ffffff" font-size="28px" font-weight="bold">
              Job Alert
            </mj-text>
            <mj-text align="center" color="#e9d5ff" font-size="16px">
              {date_str}
            </mj-text>
          </mj-column>
        </mj-section>

        <!-- Summary -->
        <mj-section padding="20px">
          <mj-column>
            <mj-text align="center" font-size="16px" color="{COLORS['text']}">
              Found <strong style="color: {COLORS['primary']}">{len(jobs)}</strong> new job(s) matching your keywords
            </mj-text>
          </mj-column>
        </mj-section>

        <!-- Job Cards -->
        {job_cards}

        <!-- Footer -->
        <mj-section padding="20px">
          <mj-column>
            <mj-divider border-color="#e5e7eb" />
            <mj-text align="center" color="{COLORS['text_light']}" font-size="12px">
              Automated email from Job Board Emailer
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-body>
    </mjml>
    """
    return template


def format_jobs_html(jobs, date_str):
    """Convert MJML template to HTML."""
    mjml_template = build_email_mjml(jobs, date_str)
    result = mjml_to_html(mjml_template)
    return result.html


def format_jobs_text(jobs):
    """Format jobs as plain text for email body."""
    if not jobs:
        return "No new jobs found this week."

    lines = []
    for job in jobs:
        lines.append(f"- {job['title']}")
        lines.append(f"  Company: {job['company']}")
        lines.append(f"  Location: {job['location']}")
        lines.append(f"  URL: {job['url']}")
        lines.append("")
    return "\n".join(lines)


def send_email(jobs):
    """Send email with job listings."""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Error: Email credentials not configured. Check your .env file.")
        return False

    date_str = datetime.now().strftime("%B %d, %Y")
    subject = f"Job Alert - {date_str}"

    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL

    # Plain text version
    text_body = f"Weekly Job Report - {date_str}\n\n"
    text_body += f"Found {len(jobs)} new job(s):\n\n"
    text_body += format_jobs_text(jobs)

    # HTML version (generated from MJML)
    html_body = format_jobs_html(jobs, date_str)

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Email sent successfully to {RECIPIENT_EMAIL}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check your email/password.")
        print("For Gmail, use an App Password: https://myaccount.google.com/apppasswords")
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


if __name__ == "__main__":
    # Test with sample data
    test_jobs = [
        {
            "title": "Python Developer",
            "company": "Tech Corp",
            "location": "Remote",
            "url": "https://example.com/job/1",
        }
    ]
    send_email(test_jobs)
