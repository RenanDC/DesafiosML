import cgi
import os
import sys
import csv
import cgitb; cgitb.enable()
import conection
import ConEmail
import base64
import ldap
import ldap.modlist as modlist

def insertldap(name,lastname, email,password):
    l = ldap.initialize("ldap://localhost:389/")

    l.simple_bind_s("cn=manager,dc=example,dc=com","secret")

    dn="cn=replica,dc=example,dc=com" 

    attrs = {}
    attrs['objectclass'] = ['top','group']
    attrs['uid'] = str(name)+"."+str(lastname)
    attrs['cn'] = name
    attrs['sn'] = lastname
    attrs['userPassword'] = password
    attrs['mail'] = email


    ldif = modlist.addModlist(attrs)

    l.add_s(dn,ldif)

    l.unbind_s()

def insertDB(name,lastname, email,password):
    try:
        conn = conection.conn()
        psw64 = base64.encodestring(password)
        query = "insert into ldapDB (ldap_name, ldap_lastname, ldap_email, ldap_senha, DT_InsertMLEMail) " \
            "VALUES(%s,%s, %s, %s, NOW())"
        
        cursor = conn.cursor()
        cursor.execute(query,(name, lastname, email, psw64))
 
        conn.commit()
    except Error as e:
        print('Error:', e)
 
    finally:
        cursor.close()
        conn.close()

def sendEmaiil(name,lastname, email,password):
    account = 'account@gmail.com'
    passwdEmail = 'passwd'

    server = ConEmail.connectSMTP(account,passwdEmail)
    msg = MIMEMultipart()
    msg['From'] = account
    msg['To'] = email
    msg['Subject'] = "Your ML Account"
     
    body = "Hi " + str(name) + "Welcome to Mercado livre \n thats yout new account:\n" + "login: " + str(email) + "\n" +"password: " + str(password)

    msg.attach(MIMEText(body, 'plain'))

    text = msg.as_string()
    server.sendmail(account, email, text)
    server.quit()

def printHeader():
    print("Content-Type: text/html")
    print()
    print("<html>")
    print("<header><title>Upload File with CGI Python</title></head>")
    print("<body>")

def printFooter():
    print("</body></html>")

def generatePWD():
    char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    while len(passwd) != 8:
        passwd = passwd + random.choice(char)

    return passwd 

printHeader()

print("<h2>Upload File Example with CGI Python</h2>")

form = cgi.FieldStorage()

fileitem = form["filename"]

if fileitem.filename:

    fn = os.path.basename(fileitem.filename)
    open("./upload/" + fn, 'wb').write(fileitem.file.read())

    with open("./upload/" + fn, 'rb') as dfile:
        #nlinhas = sum( 1 for line in dfile)
        #print(nlinhas)
        x = 0
        reader = csv.reader(dfile)
        for row in dfile:
            if x > 0:
                password = generatePWD()
                listx = row.split(";")
                sendEmaiil(listx[0],listx[1],listx[2],password)
                insertDB(listx[0],listx[1],listx[2],password)
                insertldap(listx[0],listx[1],listx[2],password)
            x+=1    

    print("<p>Total of  " + x + "user was included on OpenLDAP!</p>")

else:
    print("<p>No file was uploaded!</p>")

printFooter()
    
