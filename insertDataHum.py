import sqlite3
import sys
import datetime
import Adafruit_DHT

connection = sqlite3.connect('/var/www/lab_app/lab_app.db')
cursor = connection.cursor()

year = datetime.datetime.today().strftime('%Y')
month = datetime.datetime.today().strftime('%m')
day = datetime.datetime.today().strftime('%d')

cursor.execute("SELECT Year,Month,Day from humidityTable WHERE Year = ? AND Month = ? AND Day = ?", [year,month,day])
rowsHumidity = cursor.fetchall()

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)

if not rowsHumidity:
    cursor.execute('INSERT INTO humidityTable VALUES(?,?,?,?)',(year,month,day,humidity))
    connection.commit()
    print("Records created successfully")
    connection.close()
else:
    cursor.execute("SELECT humidity FROM humidityTable WHERE Year = ? AND Month = ? AND Day = ?", [year,month,day])
    currentHum = cursor.fetchall()
    convertedHum = currentHum[0][0]

    newHum = round(((convertedHum + humidity)/2),1)
    cursor.execute("UPDATE humidityTable SET humidity = ? WHERE Year = ? AND Month=? AND Day=?",(newHum,year,month,day))
    connection.commit()
    connection.close()
