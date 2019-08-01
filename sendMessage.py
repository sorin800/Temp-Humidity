import smtplib
import config

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject,msg)
        server.sendmail(config.EMAIL_ADDRESS,"sorintruica@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")



send_email("Alerta Mesaj!!!","Mesaj mesaj rasp")
