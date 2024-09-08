# k8s_monitor/utils/email_alerts.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from k8s_monitor.utils.email_config import EMAIL_HOST, EMAIL_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL

def send_email_alert(subject, message):
    """
    Send an email alert using SMTP.
    """
    try:
        # Set up the server connection
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Create the email content
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject

        # Add the message body
        msg.attach(MIMEText(message, 'plain'))

        # Send the email
        server.send_message(msg)
        server.quit()

        print(f"Email alert sent to {RECIPIENT_EMAIL}")

    except Exception as e:
        print(f"Failed to send email alert: {str(e)}")
