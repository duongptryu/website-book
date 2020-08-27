import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy.sql import expression

def sendmail(recieve_mail, new_password):
    mail_content = '''Test mail'''
    #The mail addresses and password
    sender_address = 'duongptryu@gmail.com'
    sender_pass = 'A201085a'
    receiver_address = recieve_mail
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    try:
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
    except expression as identifier:
        return False
    return True
    
