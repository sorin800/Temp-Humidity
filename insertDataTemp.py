import sqlite3
import sys
import datetime
import Adafruit_DHT

connection = sqlite3.connect('/var/www/lab_app/lab_app.db')
cursor = connection.cursor()

year = datetime.datetime.today().strftime('%Y')
month = datetime.datetime.today().strftime('%m')
day = datetime.datetime.today().strftime('%d')

cursor.execute("SELECT Year,Month,Day from tempTable WHERE Year = ? AND Month = ? AND Day = ?", [year,month,day])
rowsTemp = cursor.fetchall()

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)

if not rowsTemp:
    cursor.execute('INSERT INTO tempTable VALUES(?,?,?,?)',(year,month,day,temperature))
    connection.commit()
    print("Records created successfully")
    connection.close()
else:
    cursor.execute("SELECT temp FROM tempTable WHERE Year = ? AND Month = ? AND Day = ?", [year,month,day])
    currentTemp = cursor.fetchall()
    convertedTemp = currentTemp[0][0]
    newTemp = round(((convertedTemp + temperature)/2),1)
    cursor.execute("UPDATE tempTable SET temp = ? WHERE Year = ? AND Month=? AND Day=?",(newTemp,year,month,day))
    connection.commit()
    connection.close()

