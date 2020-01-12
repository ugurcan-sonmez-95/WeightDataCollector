from email.mime.text import MIMEText
import smtplib

### Sends the weight data to the user e-mail
def send_email(s_email, s_weight, average_weight, s_count):
    from_email = "email@email.com"
    from_password = "password"
    to_email = s_email

    subject = "Weight Statistics"
    message = f"Hello. Your weight is <strong>{s_weight}</strong> kg. <br>The average weight of all is <strong>{average_weight}</strong> kg and it was calculated out of <strong>{s_count}</strong> user(s). <br>Thank you for using the app!"

    msg = MIMEText(message, 'html')

    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = from_email

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)