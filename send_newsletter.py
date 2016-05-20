import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

def send_email(sender_data, receivers, message):

    sender, password = sender_data

    smtp_host = 'smtp.live.com'        # microsoft
    #smtp_host = 'smtp.gmail.com'       # google
    #smtp_host = 'smtp.mail.yahoo.com'  # yahoo

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Taekwondo Newsletter"
    msg['From'] = sender
    msg['To'] = ", ".join(receivers)
    msg.attach( MIMEText(message, 'html') )

    smtp_obj = smtplib.SMTP(smtp_host, 587, timeout=10)

    try:
        smtp_obj.starttls()
        smtp_obj.login(sender, password)
        smtp_obj.sendmail(sender, receivers, msg.as_string())

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
