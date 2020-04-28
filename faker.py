import psycopg2
import json
import time
from psycopg2.extras import RealDictCursor
conn = psycopg2.connect(host="localhost", database="hardwarex", user="postgres", password="123456", cursor_factory=RealDictCursor)
cursor = conn.cursor()

def seedTable():
    deleteCommands = ("DROP TABLE IF EXISTS stations","DROP TABLE IF EXISTS bins","DROP TABLE IF EXISTS ip_ports","DROP TABLE IF EXISTS users","DROP TABLE IF EXISTS fake_bins_weight")
    for deletecommand in deleteCommands:
        cursor.execute(deletecommand)
    commands = ("CREATE TABLE stations (id serial  NOT NULL PRIMARY KEY,type VARCHAR (50),category VARCHAR (50),rotation VARCHAR (50), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())","CREATE TABLE ip_ports (id serial  NOT NULL PRIMARY KEY,ip VARCHAR (50),port VARCHAR (50),name VARCHAR (50),station_id INT, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())","CREATE TABLE users (id serial  NOT NULL PRIMARY KEY,username VARCHAR (50),password VARCHAR (50), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())","CREATE TABLE bins (id serial  NOT NULL PRIMARY KEY,name VARCHAR (50),status VARCHAR (50),station_id INT,position INT, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())","CREATE TABLE fake_bins_weight (id serial  NOT NULL PRIMARY KEY,bin_id VARCHAR (50),weight NUMERIC, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())")
    for command in commands:
        cursor.execute(command)
    conn.commit()
    print("Table Add Successful")
   
   

def seedData():
    # stations
    cursor.execute("insert into stations (type, rotation) values (%s, %s) RETURNING id", ("INBOUND", "C"))
    cursor.execute("insert into stations (type, rotation) values (%s, %s) RETURNING id", ("INBOUND", "A"))
    cursor.execute("insert into stations (type, rotation) values (%s, %s) RETURNING id", ("INBOUND", "A"))

    # bins
    cursor.execute("insert into bins (name, status, station_id, position) values (%s, %s, %s, %s) RETURNING id", ("MY001-ST0002", "", 1, 1))
    cursor.execute("insert into bins (name, status, station_id, position) values (%s, %s, %s, %s) RETURNING id", ("MY001-ST0004", "", 1, 3))
    cursor.execute("insert into bins (name, status, station_id, position) values (%s, %s, %s, %s) RETURNING id", ("MY001-ST0005", "", 1, 4))

    # ip_ports
    cursor.execute("insert into ip_ports (ip, port, name, station_id) values (%s, %s, %s, %s) RETURNING id", ("192.168.11.25", "4000", "PLC3", 3))
    cursor.execute("insert into ip_ports (ip, port, name, station_id) values (%s, %s, %s, %s) RETURNING id", ("192.168.11.23", "4000", "PLC2", 2))
    cursor.execute("insert into ip_ports (ip, port, name, station_id) values (%s, %s, %s, %s) RETURNING id", ("192.168.11.20", "4000", "PLC1", 1))


     # users
    cursor.execute("insert into users (username, password) values (%s, %s) RETURNING id", ("han", "123456"))
    cursor.execute("insert into users (username, password) values (%s, %s) RETURNING id", ("yilee", "123456"))
    cursor.execute("insert into users (username, password) values (%s, %s) RETURNING id", ("zhijian", "123456"))
    conn.commit()
    print("Data Add Successful")



if __name__ == "__main__":
    seedTable()
    seedData()
  

  # [ faker ] -> command - python faker.py



