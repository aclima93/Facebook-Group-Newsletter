import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_data, receivers, message):

    sender, password = sender_data

    if "gmail" not in sender:
        print("Error: Only gmail senders are supported by this script.")
        return

    smtp_host = 'smtp.gmail.com'       # google

    to = [sender]
    cc = [sender]
    bcc = receivers

    msg = MIMEMultipart('alternative')
    msg.add_header('Subject', 'Taekwondo Newsletter')
    msg.add_header('From', sender)
    msg.add_header('To', ','.join(to))
    msg.add_header('Cc', ','.join(cc))
    msg.add_header('Bcc', ','.join(bcc))
    msg.attach( MIMEText(message, 'html') )

    smtp_obj = smtplib.SMTP(smtp_host, 587, timeout=10)

    try:
        smtp_obj.starttls()
        smtp_obj.login(sender, password)
        smtp_obj.sendmail(sender, to + cc + bcc, msg.as_string())

        print("Successfully sent email")

    except Exception:
        print("Error: unable to send email")

    finally:
        smtp_obj.quit()


def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '').strip()


def file2string_list(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace('\n', '').strip()
        return lines


if __name__ == "__main__":

    sender_data = file2string_list(sys.argv[1])
    receivers = file2string_list(sys.argv[2])
    message = file2string(sys.argv[3])

    send_email(sender_data, receivers, message)
