import sys
sys.dont_write_bytecode = True


import smtplib
import markdown
from email import encoders
from pydantic import EmailStr
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from typing import List, Optional, Dict, Any
from email.mime.multipart import MIMEMultipart

class SendMail:
    """
    A model to send emails with optional attachments.
    """
    def __init__(self, sender_email: str, sender_password: str, smtp_server: str, smtp_port: int) -> None:
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_mail(self, recipients: List[EmailStr], subject: str, body: str, mail_cc: Optional[List[EmailStr]] = None, attachment: Optional[str] = None, attachment_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Send the email using the SMTP server details.
        """
        try:
            # Prepare the email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = ",".join(recipients)
            if mail_cc:
                msg['CC'] = ",".join(mail_cc)
            msg.preamble = 'Multipart message.\n'

            # Convert Markdown body to HTML and attach it
            if body:
                html_body = markdown.markdown(body)
                part_body = MIMEText(html_body, 'html')
                msg.attach(part_body)

            # Attach the file if provided
            if attachment:
                try:
                    part = MIMEBase('application', "octet-stream")
                    with open(attachment, "rb") as file:
                        part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={attachment_name or attachment}')
                    msg.attach(part)
                except Exception as err:
                    return {"status": "error", "message": f"Error attaching file: {err}"}

            # Send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipients + (mail_cc or []), msg.as_string())

            return {"status": "success", "message": "Email Sent"}

        except Exception as err:
            return {"status": "error", "message": f"Error while sending mail: {err}: Enabling the `Less secure app access` option in your Gmail account settings may help resolve this issue."}