"""
Created on September 12, 2020
Author: Richard Punt
Version: Python 3.8
Description: Queries for Graph class

"""

# Drop Airports table
drop_airports = """
DROP TABLE IF EXISTS Airports;
"""

# Create Airports table
create_airports = """
CREATE TABLE Airports (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Airport TEXT,
City TEXT,
State TEXT,
Longitude FLOAT,
Latitude FLOAT,
xCoordinate FLOAT,
yCoordinate FLOAT);
"""

# Insert elements into Airports table
insert_airport = """
INSERT INTO Airports (Airport, City, State, Longitude, Latitude, xCoordinate, yCoordinate)
VALUES (?, ?, ?, ?, ?, ?, ?);
"""

select_airport_list = """
SELECT Airport FROM Airports
"""

# Drop Flights table
drop_flights = """
DROP TABLE IF EXISTS Flights;
"""

# Create Flights table
create_flights = """
CREATE TABLE Flights (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Flight_Number TEXT,
Operator TEXT,
From_Airport TEXT,
To_Airport TEXT,
Depart Time,
Arrival Time);
"""

# Insert elements into Flights table
insert_flight = """
INSERT INTO Flights (Flight_Number, Operator, From_Airport, To_Airport, Depart, Arrival)
VALUES (?, ?, ?, ?, ?, ?);
"""

# Select all Flight_Number and To_Airport from Flights table based on From_Airport
select_flights_from_airport = """
SELECT Flight_Number, To_Airport FROM Flights WHERE From_Airport = ?
"""

# Select Depart from Flights table based on Flight_Number
select_depart_from_flight = """
SELECT Depart FROM Flights WHERE Flight_Number = ?
"""

# Select Arrival from Flights table based on Flight_Number
select_arrival_from_flight = """
SELECT Arrival FROM Flights WHERE Flight_Number = ?
"""




