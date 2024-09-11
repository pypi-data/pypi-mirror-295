from imaplib import IMAP4_SSL, IMAP4
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import decode_header
from email import encoders, message_from_bytes
from typing import List, Optional, Dict
from re import sub
from os import makedirs
from os.path import join

def smtp(to_emails:List[str], 
         smtp_port:int, 
         smtp_server:str, 
         sender_email:str, 
         sender_password:str, 
         subject:str,
         body:str,
         body_type:str,
         attachments: Optional[Dict[str,str]] = None,
         cc_emails:Optional[List[str]] = []
         ) -> None:
        
    message = MIMEMultipart()
    message['From'] = sender_email
    message['Subject'] = subject
    message['To'] = ", ".join(to_emails)
    message['Cc'] = ", ".join(cc_emails)
    message.attach(MIMEText(body, body_type))
    all_recipients = to_emails + cc_emails

    if attachments:
        for attachment_name, attachment_path in attachments.items():
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={attachment_name}",)
                message.attach(part)

            except Exception as error:
                print(f"Error: The file {attachment_path} was not found.")
                print(f"Error: {error}")
                return
    try:
        server = SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, all_recipients, message.as_string())
    except Exception as error:
        print("Email not sent.")
        print(f"Error: {error}")
    finally:
        server.quit()
        return



def imap(
    imap_port: int,
    imap_server: str,
    email_account: str,
    password: str,
    download_folder: str,
    mailbox: str = 'inbox',
    search_criteria: str = 'ALL'
    ) -> None:
    

    body = ""

    try:
        if imap_port == 993:
            mail = IMAP4_SSL(imap_server)
        elif imap_port == 143:
            mail = IMAP4(imap_server)
            mail.starttls()

        mail.login(email_account, password)
        mail.select(mailbox)
        print(f"Connected to {mailbox} on {imap_server}")
    except Exception as error:
        print("Possible wrong port number or IMAP server")
        print(f"Error connecting to the IMAP server: {error}")
        return

    try:
        result, data = mail.search(None, search_criteria)
        if result == 'OK':
            for num in data[0].split():
                result, data = mail.fetch(num, '(RFC822)')
                if result == 'OK':
                    email_message = message_from_bytes(data[0][1])
                    subject, encoding = decode_header(email_message['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    
                    clean_subject = sub(r'[^\w\-_\. ]', "_", subject)
                    email_folder = join(download_folder, clean_subject)
                    makedirs(email_folder, exist_ok=True)

                    if email_message.is_multipart():
                        for part in email_message.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True).decode(part.get_content_charset())
                                break
                    else:
                        body = email_message.get_payload(decode=True).decode(email_message.get_content_charset())

                    email_text_file = join(email_folder, f"{num.decode('utf-8')}.txt")
                    with open(email_text_file, 'w', encoding='utf-8') as f:
                        f.write(f"Subject: {subject}\n")
                        f.write(f"Body:\n{body}")

                    for part in email_message.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
                        file_name = part.get_filename()
                        if file_name:
                            filepath = join(email_folder, file_name)
                            with open(filepath, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                            print(f"Attachment {file_name} downloaded to {filepath}")
        else:
            print("No emails found.")
    except Exception as error:
        print(f"Error retrieving emails: {error}")
    finally:
        mail.logout()