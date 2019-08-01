from flask import Flask, request, render_template
import sys
import sqlite3
import Adafruit_DHT
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging

@app.route("/")
def hello():
        return "Hello World!"

@app.route("/lab_temp")
def lab_temp():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
    if humidity is not None and temperature is not None:
        return render_template("lab_temp.html",temp=temperature,hum=humidity)
    else:
        return render_template("no_sensor.html")

@app.route("/home", methods=['GET'])
def home():

    conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
    curs=conn.cursor()

    curs.execute("SELECT * FROM tempTable")
    temperatures = curs.fetchall()
    curs.execute("SELECT * FROM humidityTable")
    humidities = curs.fetchall()
    
    currentYear = datetime.today().strftime('%Y')
    currentMonth =datetime.today().strftime('%m')
    currentDay = datetime.today().strftime('%d')
    
    year7Days = (datetime.now() + timedelta(days=7)).strftime('%Y')
    month7Days = (datetime.now() + timedelta(days=7)).strftime('%m')
    day7Days = (datetime.now() + timedelta(days=7)).strftime('%d')

    
    curs.execute("SELECT Year,Month,Day,PredictedTemp,PredictedHum FROM predictionsTable WHERE Year BETWEEN ? And ? AND  Month BETWEEN ? AND ? AND Day BETWEEN ? AND ?"
                        ,(currentYear,year7Days,currentMonth,month7Days,currentDay,day7Days))
    predictions = curs.fetchall()

    conn.close()
    if not temperatures and not humidities and not predictions:
        return render_template("no_sensor.html")
        
    return render_template("home.html",temp=temperatures, hum=humidities, pred=predictions, temp_items= len(temperatures),hum_items= len(humidities))

@app.route("/search", methods=['GET'])
def search():

    fromDate = request.args.get('from')
    to = request.args.get('to')
    
    monthFrom = fromDate[0:2]
    dayFrom = fromDate[3:5]
    yearFrom = fromDate[6:10]
    
    monthTo = to[0:2]
    dayTo = to[3:5]
    yearTo = to[6:10]

    currentYear = datetime.today().strftime('%Y')
    currentMonth =datetime.today().strftime('%m')
    currentDay = datetime.today().strftime('%d')

    conn=sqlite3.connect('/var/www/lab_app/lab_app.db')
    curs=conn.cursor()
   
    year7Days = (datetime.now() + timedelta(days=7)).strftime('%Y')
    month7Days = (datetime.now() + timedelta(days=7)).strftime('%m')
    day7Days = (datetime.now() + timedelta(days=7)).strftime('%d')

    curs.execute("SELECT Year,Month,Day,temp FROM tempTable WHERE Year BETWEEN ? AND ? And Month BETWEEN ? AND ? AND Day BETWEEN ? AND ?",(yearFrom,yearTo,monthFrom,monthTo,dayFrom,dayTo))
    temperatures = curs.fetchall()
    curs.execute("SELECT Year,Month,Day,humidity FROM humidityTable WHERE Year BETWEEN ? AND ? And Month BETWEEN ? AND ? AND Day BETWEEN ? AND ?",(yearFrom,yearTo,monthFrom,monthTo,dayFrom,dayTo))
    humidities = curs.fetchall()
    #pred = predictions
    curs.execute("SELECT Year,Month,Day,PredictedTemp,PredictedHum FROM predictionsTable WHERE Year BETWEEN ? And ? AND  Month BETWEEN ? AND ? AND Day BETWEEN ? AND ?"
            ,(currentYear,year7Days,currentMonth,month7Days,currentDay,day7Days))
    predictions = curs.fetchall()
    #pred = predictions
    conn.close()
    if not temperatures and not humidities and not predictions:
        return render_template("no_sensor.html")
        
    return render_template("home.html",temp=temperatures, hum=humidities, pred=predictions, temp_items= len(temperatures),hum_items= len(humidities))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
