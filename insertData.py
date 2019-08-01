import sqlite3
import sys
import datetime
import Adafruit_DHT

connection = conn=sqlite3.connect('/var/www/lab_app/lab_app.db')

cursor = connection.cursor()

dateNow = datetime.datetime.today().strftime('%Y-%m-%d')

cursor.execute("SELECT DatetimeIot FROM temperature WHERE DatetimeIot = ?", [dateNow])

rows = cursor.fetchall()
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)

if not rows:
    cursor.execute('INSERT INTO temperature values(?,?)', (dateNow,temperature))
    connection.commit()
    print("Records created successfully")
    connection.close()
else:
    cursor.execute("SELECT temp FROM temperature WHERE DatetimeIot = ?", [dateNow])
    currentTemp = cursor.fetchall()
    convertedTemp = currentTemp[0][0]
    newTemp = round((convertedTemp + temperature) / 2)
    cursor.execute("UPDATE temperature SET temp = ? WHERE DatetimeIot = ?", (newTemp, dateNow))
    connection.commit()
    connection.close()
