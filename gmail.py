import datetime
import timestring
import conection
import numpy
import email
import ConEmail

def searchDevOPS(mail):
    result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
    i = len(data[0].split())
    partemail = []
    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        # result, email_data = conn.store(num,'-FLAGS','\\Seen')
        # this might work to set flag to seen, if it doesn't already
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # Header Details
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" %(str(local_date.strftime("%Y-%m-%d %H:%M:%S")))
        email_date = str(email.header.make_header(email.header.decode_header(email_message['Date'])))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

        if subject.upper().find('DEVOPS') > -1 or str(email_message).upper().find('DEVOPS') > -1:
            #print(email_date + "\n")
            #print(email_from + "\n")
            #print(subject + "\n")
            email_date = datetime.datetime.strptime(email_date[:-6],"%a, %d %b %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            partemail.insert(x,(email_date, email_from, subject))

    return partemail

def insertEmail(infos):
    try:
        conn = conection.conn()
        
        query = "insert into mlemail_tb (DT_Email, From_Email, Subject_Email, DT_InsertMLEMail) " \
            "VALUES(%s,%s, %s, NOW())"
        
        cursor = conn.cursor()
        cursor.executemany(query, infos)
 
        conn.commit()
    except Error as e:
        print('Error:', e)
 
    finally:
        cursor.close()
        conn.close()

def main():
    mail = ConEmail.connectEmail('account@gmail.com','passwd')
    infoemail = searchDevOPS(mail)
    insertEmail(infoemail)
    print("Total de " + str(len(infoemail)) + " Emails foram inseridos.")


main()