import sys
sys.path.append('../BrewDB')
from flask import Flask, render_template, request, redirect
from flask import Markup
import DB
import datetime
import json


app = Flask(__name__)

@app.route("/")
def home():
   return graph("all")

@app.route("/<dataset>")
def graph(dataset):
   if(dataset=="daily"):
      chartData = create_chart_data(DB.get_daily_data()) 
   elif(dataset=="hourly"):
      chartData = create_chart_data(DB.get_hourly_data()) 
   elif(dataset=="last_week"):
      chartData = create_chart_data(DB.get_last_week_data()) 
   elif(dataset=="last_day"):
      chartData = create_chart_data(DB.get_last_day_data()) 
   elif(dataset=="last_hour"):
      chartData = create_chart_data(DB.get_last_hour_data())
   else:
      chartData = create_chart_data(DB.get_all_data())
   templateData = {
      'title' : 'Lombok Brews Climate Control',
      'labels': chartData["labels"],
      'temperature': chartData["temperature"],
      'min': chartData["min"],
      'max': chartData["max"]
      }
   return render_template('index.html', **templateData)

def create_chart_data(items):
   chartData = {"labels": [], "temperature": [], "min": [], "max": []}
   for item in items:
      chartData["labels"].append(item[0])
      chartData["temperature"].append(item[1])
      chartData["min"].append(item[2])
      chartData["max"].append(item[3])
   return chartData

@app.route("/setup_get")
def setup_get():
   programs = DB.get_program()
   programData = {
      'title' : 'Lombok Brews Setup Climate',
      'items': programs
   }
   return programData

@app.route("/setup_set")
def setup_set():
   min = request.args.get('min', 0, type=float)
   max = request.args.get('max', 0, type=float)
   start = request.args.get("start", datetime.datetime.now(), type=datetime)
   DB.set_program({"min": min, "max": max, "start": start})
   return setup_get()

@app.route("/clear")
def clear():
   DB.clear_data()
   return redirect("/setup")

@app.route("/start")
def start():
   DB.start_program()
   return redirect("/setup")

@app.route("/stop")
def stop():
   DB.stop_program()
   return redirect("/setup")

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)


