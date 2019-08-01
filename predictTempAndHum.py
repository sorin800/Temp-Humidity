import pandas as pd
import numpy as np
import sqlite3
import sys
import csv
import smtplib
import config
from sklearn import linear_model
from datetime import datetime
from datetime import timedelta


conn = sqlite3.connect('/var/www/lab_app/lab_app.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM tempTable")

def send_email(subject,msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject,msg)
        server.sendmail(config.EMAIL_ADDRESS,"sorintruica@gmail.com",message)
        server.quit()
        print("Seucces: Email sent!")
    except:
        print("Email failde to send.")

with open("out.csv", "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description])  # write headers
    csv_writer.writerows(cursor)

for i in range(1, 8):
    date_now_more_7_days = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
    print("Data pentru predictie este: " + str(date_now_more_7_days))
    year = int(date_now_more_7_days.split("-")[0])
    month = int(date_now_more_7_days.split("-")[1])
    date = int(date_now_more_7_days.split("-")[2])
    df = pd.read_csv('out.csv')
    reg = linear_model.LinearRegression()
    reg.fit(df[['Year', 'Month', 'Day']], df.temp)
    prediction = reg.predict([[year, month, date]])

    print(np.round(prediction[0]))

    if(np.round(prediction[0]) < 0):
        send_email("Alerta Senzor","Temperatura este sub 0 grade")

    if(np.round(prediction[0]) > 35):
        send_email("Alerta Senzor","Temperatura este mai mare de 35 de grade")
    
    cursor.execute('INSERT INTO predictionsTable VALUES(?,?,?,?,?)',(year,month,date,(np.round(prediction[0])),0))
    #conn.commit()

cursor.execute("SELECT * FROM humidityTable")

with open("outHum.csv", "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description])
    csv_writer.writerows(cursor)

for i in range(1,8):
    dateNow7Days = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
    #print("Data pentru predictia Umiditatii este: " + str(dateNow7Days))
    year = int(dateNow7Days.split("-")[0])
    month = int(dateNow7Days.split("-")[1])
    date = int(dateNow7Days.split("-")[2])
    df = pd.read_csv('outHum.csv')
    reg = linear_model.LinearRegression()
    reg.fit(df[['Year','Month','Day']],df.humidity)
    predictHum = reg.predict([[year, month, date]])
    
    if(np.round(predictHum[0]) < 5):
        send_email("Alerta Senzor Umiditate", "Umiditate este sub 5%")

    if(np.round(predictHum[0]) > 75):
        send_email("Alerta Senzor Umiditate","Umiditatea este foarte crescuta peste 75%")

    #print("Predictia pe umiditate este: " + str(np.round(predictHum[0])))
    cursor.execute("UPDATE predictionsTable SET PredictedHum = ? WHERE Year = ? AND Month=? AND Day=?",((np.round(predictHum[0]),year,month,date)))
    
   # conn.commit()
    

conn.commit()    
conn.close()
