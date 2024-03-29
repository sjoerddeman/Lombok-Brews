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
   chartData = create_chart_data(DB.get_all_data())
   templateData = {
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
      'items': programs
   }
   return json.dumps(programData)

@app.route("/setup_set", methods=['GET', 'POST'])
def setup_set():
   if request.method == "POST":
      item = request.form
      print(str(item))
      max = item['max']
      min = item['min']
      start = datetime.datetime.strptime(item['start'], "%Y-%m-%dT%H:%M")
      DB.set_program({"min": min, "max": max, "start": start})
   return setup_get()

@app.route("/clear")
def clear():
   DB.clear_data()
   return redirect("/")

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


