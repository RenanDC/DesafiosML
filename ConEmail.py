import imaplib
import smtplib
import mailbox

def connectEmail(account, passwd):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(account, passwd)
    mail.list()
    mail.select()

    return mail

def connectSMTP(account, passwd):
	server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(account, passwd)

