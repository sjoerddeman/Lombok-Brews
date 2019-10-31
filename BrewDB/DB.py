import sqlite3
import sys
from datetime import datetime


# function to insert data on a table
def add_data (temp, min, max):
    now = datetime.now()
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO temp_data values((?), (?), (?), (?))", (now,temp,min,max))
    conn.commit()
    conn.close()

# get database content
def get_all_data():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    list = []
    for row in curs.execute("SELECT * FROM temp_data"):
        list.append(row)
    conn.close()
    return list;

# clear table
def clear_data ():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    curs.execute("DROP TABLE temp_data")
    curs.execute("CREATE TABLE temp_data(timestamp DATETIME, temp NUMERIC, min NUMERIC, max NUMERIC)")
    curs.execute("DROP TABLE program")
    curs.execute("CREATE TABLE program(min NUMERIC, max NUMERIC, start DATETIME)")
    conn.commit()
    conn.close()
    
def set_program (item):
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO program values((?), (?), (?))", (float(item["min"]), float(item["max"]), item["start"]))
    conn.commit()
    conn.close()
  
def get_program ():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    program = []
    for row in curs.execute("SELECT * FROM program"):
        program.append(row)
    conn.close()
    return program;
    

def get_current_program_item(items):
	current_item = []
	for item in items:
		if(datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S") <= datetime.now()):
			current_item = item
	return current_item
