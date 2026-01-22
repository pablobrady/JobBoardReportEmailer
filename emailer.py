import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    RECIPIENT_EMAIL,
    SMTP_SERVER,
    SMTP_PORT,
)


def format_jobs_html(jobs):
    """Format jobs as HTML for email body."""
    if not jobs:
        return "<p>No new jobs found this week.</p>"

    html = "<ul>"
    for job in jobs:
        html += f"""
        <li style="margin-bottom: 15px;">
            <strong>{job['title']}</strong><br>
            Company: {job['company']}<br>
            Location: {job['location']}<br>
            <a href="{job['url']}">View Job</a>
        </li>
        """
    html += "</ul>"
    return html


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
    subject = f"Weekly Job Alert - {date_str}"

    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL

    # Plain text version
    text_body = f"Weekly Job Report - {date_str}\n\n"
    text_body += f"Found {len(jobs)} new job(s):\n\n"
    text_body += format_jobs_text(jobs)

    # HTML version
    html_body = f"""
    <html>
    <body>
        <h2>Weekly Job Report - {date_str}</h2>
        <p>Found <strong>{len(jobs)}</strong> new job(s):</p>
        {format_jobs_html(jobs)}
        <hr>
        <p style="color: gray; font-size: 12px;">
            This is an automated email from your Weekly Job Emailer.
        </p>
    </body>
    </html>
    """

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
