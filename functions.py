import re
import smtplib
import sqlite3
from passlib import hash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database configuration
DB = sqlite3.connect('database.db', check_same_thread=False)
cursor = DB.cursor()


def send_email( Subject='Test Email', Message='This is a test email'):
    mail = sender
    passwrd = password
    send_to = reciever
    subject = Subject
    message = Message
    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = send_to
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(mail, passwrd)
        text = msg.as_string()
        server.sendmail(mail, send_to, text)
        msg = "ok"
    except Exception as err:
        msg = f"Something went wrong:" \
              f"Error: {str(err)}"
    return msg


def htmlmessage(name, email, message):
    html = f"""<html lang="en" style="padding: 0 ;margin: 0; box-sizing: border-box;">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
    <div style="border: 1px solid rgb(163, 0, 0);background: linear-gradient(75deg, white, rgba(241, 195, 195, 
    0.645)); border-radius: 10px; padding: 20px; padding-bottom: 5px; margin: 30px; box-shadow: 7px 5px 7px 0px grey;"> 
        <div style="border-bottom: 1px solid rgb(163, 0, 0); padding-bottom: 5px;">
            <h1
                style="text-align: center; margin-top: 0px; margin-bottom: 10px; font-size: 30px; border-bottom: 1px 
                solid rgb(163, 0, 0);"> 
                Feedback</h1>
            <div style="letter-spacing: 0.8px;">
                <i style="font-style: normal; text-transform: uppercase; font-weight: 600; font-size: 15px;"> <span
                        style="font-size: 20px;">u</span>sername: </i>
                <i style="font-style: normal; font-size: 15px;"> {name}</i>
            </div>
            <div style="letter-spacing: 0.5px;">
                <i style="font-style: normal; text-transform: uppercase; font-weight: 600; font-size: 15px;"> <span
                        style="font-size: 20px;">e</span>-mail: </i>
                <i style="font-style: normal; font-size: 15px;"> <a href="mailto:{email}" style="color: rgb(163, 0, 0); "> {email} </a></i> 
            </div>
            <div style="letter-spacing: 0.5px;">
                <i style="font-style: normal; text-transform: uppercase; font-weight: 600; font-size: 15px;"> <span
                        style="font-size: 20px;">M</span>essage: </i> <br>
                <i
                    style="font-style: normal; font-size: 15px; letter-spacing: 0.1px; display: inline-block; 
                    padding: 5px;"> 
                    {message} </i>
            </div>
        </div>
        <div>
            <i style="display: block; text-align: center; padding-bottom: 0px; padding-top: 2px; font-size: 12px;">Copyright&copy;.
                All rights reserved. <span style="color: transparent;">gi</span>For more inquiry visit <a href="copyright.com" style="color: rgb(163, 0, 0); ">copyright.com </a></i></i> 
        </div>
    </div>
</body>

</html>"""
    return html


def inp(value):
    value = value.strip()
    return value


def lw_inp(value):
    value = value.strip()
    return value.lower()


def emailCheck(data):
    if data:
        email = False
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', data)
        if match != None:
            email = True
        return email


def password(password):
    password = hash.sha512_crypt.encrypt(password)
    return password


def verify(password, dbpass):
    newpass = str(password)
    return hash.sha512_crypt.verify(newpass, dbpass)


def db_insert(table, columns, values):
    sql = f"""INSERT INTO {table} ({columns}) VALUES ({values})"""
    try:
        cursor.execute(sql)
        DB.commit()
        # DB.close()
        msg = 'ok'
    except Exception as err:
        msg = str(err)
        print(f"SQL INSERT ERROR: {msg}", sql)
        return msg
    return msg


def db_delete(table, condition):
    sql = f"""DELETE FROM {table} {condition}"""
    try:
        cursor.execute(sql)
        # print(sql)
        DB.commit()
        # DB.close()
        msg = 'ok'
    except Exception as err:
        msg = str(err)
        print(f"SQL DELETE ERROR: {msg}", sql)
        return msg
    return msg


def db_select(table, what="*", conditions=''):
    sql = f"""SELECT {what} FROM {table} {conditions}"""

    try:
        result = cursor.execute(sql)
        msg = result.fetchall()
    except Exception as err:
        msg = str(err)
        print(f"SQL INSERT ERROR: {msg}", sql)
    return msg


def db_sel_columns(table, what="*", conditions=''):
    sql = f"""SELECT {what} FROM {table} {conditions}"""

    try:
        result = cursor.execute(sql)
        msg = list(map(lambda x: x[0], cursor.description))

    except Exception as err:
        msg = str(err)
        print(f"SQL INSERhT ERROR: {msg}", sql)
    return msg
