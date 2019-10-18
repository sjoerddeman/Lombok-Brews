import sqlite3
import sys


# function to insert data on a table
def add_data (temp, min, max):
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    curs.execute("INSERT INTO temp_data values(datetime('now'), (?), (?), (?))", (temp,min,max))
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
    
# get database content per day
def get_daily_data():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    list = []
    for row in curs.execute("SELECT * FROM temp_data WHERE rowid % 1440 = 0"):
        list.append(row)
    print(list)
    conn.close()
    return list;
    
# get database content per hour
def get_hourly_data():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    list = []
    for row in curs.execute("SELECT * FROM temp_data WHERE rowid % 60 = 0"):
        list.append(row)
    conn.close()
    return list;
    
# get database content last week
def get_last_week_data():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    list = []
    for row in curs.execute("SELECT * FROM (SELECT * FROM temp_data WHERE rowid % 180 = 0 ORDER BY timestamp DESC LIMIT 56) ORDER BY timestamp ASC"):
        list.append(row)
    conn.close()
    return list;

# get database content last day
def get_last_day_data():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    list = []
    for row in curs.execute("SELECT * FROM (SELECT * FROM temp_data WHERE rowid % 30 = 0 ORDER BY timestamp DESC LIMIT 48) ORDER BY timestamp ASC"):
        list.append(row)
    conn.close()
    return list;
    
# get database content last hour
def get_last_hour_data():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    list = []
    for row in curs.execute("SELECT * FROM (SELECT * FROM temp_data ORDER BY timestamp DESC LIMIT 60) ORDER BY timestamp ASC"):
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
    
def start_program ():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    curs.execute("UPDATE program SET started = TRUE")
    conn.commit()
    conn.close()
    
def stop_program ():
    conn=sqlite3.connect('../BrewDB/brewData.db')
    curs=conn.cursor()
    curs.execute("UPDATE program SET started = FALSE")
    conn.commit()
    conn.close()
