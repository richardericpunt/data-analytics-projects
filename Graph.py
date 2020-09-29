"""
Created on September 12, 2020
Author: Richard Punt
Version: Python 3.8
Description: The Graph class implements a database based on an excel file and uses this database to determine the shortest path

"""

from pandas import read_excel
import Queries as Q
import sqlite3
from datetime import *


class Graph(object):

    # (Overload) Graph Constructor
    # path = path to excel file
    # db = name of database file
    def __init__(self, path, db):

        # Create dataframe with excel file
        airport_data = read_excel(path, sheet_name='Airport Data')
        flight_data = read_excel(path, sheet_name='Flight Data')

        # Connect the database and create a cursor
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

        # Create Airport table and insert data from airport_data
        self.c.execute(Q.drop_airports)
        self.c.execute(Q.create_airports)
        for i in range(0, len(airport_data["Airport"])):
            self.c.execute(Q.insert_airport, (airport_data["Airport"][i], airport_data["City"][i], airport_data["State"][i], airport_data["longitude"][i], airport_data["latitude"][i], airport_data["x"][i], airport_data["y"][i]))
        self.conn.commit()

        # Create Flight table and insert data from flight_data
        self.c.execute(Q.drop_flights)
        self.c.execute(Q.create_flights)
        for i in range(0, len(flight_data["flight number"])):
            self.c.execute(Q.insert_flight, (flight_data["flight number"][i], flight_data["Operator"][i], flight_data["From"][i], flight_data["To"][i], str(flight_data["Depart"][i]), str(flight_data["Arrival"][i])))
        self.conn.commit()

        # Close database connection
        self.conn.close()

    # Recursive backtracking to determine all possible paths from start node id to end node id
    # start_id = start Node ID
    # end_id = end Node ID
    # actual_start_id = start Node ID repeated (used for recursive backtracking)
    # flight=None = flight number (used for recursive backtracking)
    # path=[] = path (used for recursive backtracking)
    def find_paths(self, start_id, end_id, actual_start_id, flight=None, path=[]):

        # Set ID values as string to accommodate both str inputs and int inputs
        start_id = str(start_id)
        end_id = str(end_id)
        actual_start_id = str(actual_start_id)

        # 'path' list is appended with flight and start_id
        path = path + [flight]
        path = path + [start_id]

        # If the path has the desired start and end nodes 'paths' is set to path
        # 'actual_start_id' is used to keep the original start_id because it will change with the recursion
        paths = []
        if path[1] == actual_start_id and path[-1] == end_id:
            paths = [path]

        # Obtain list of flight numbers and destination cities attached to start_id
        connecting_flights = self.get_flights_from_airport(start_id)

        # Executes find_paths for each attached node not in the path
        # This returns 'new_paths' with all the paths connected to that node until there are no more paths to explore
        # is_later checks that the next flight does not depart before the previous flight arrives
        for flight in connecting_flights:
            if flight[1] not in path: # and self.is_later(path[-2], flight[0]): - This code tests if it is possible on the same day
                new_paths = self.find_paths(flight[1], end_id, actual_start_id, flight[0], path)
                for new_path in new_paths:
                    paths.append(new_path)

        return paths

    # Uses the find_paths method to determine the shortest path based on travel duration
    # start_id = start Node ID
    # end_id = end Node ID
    def find_shortest_path(self, start_id, end_id):

        # Find all possible paths
        paths = self.find_paths(start_id, end_id, start_id)

        if paths == []:
            return []

        # Determine the duration of each possible path
        path_durations = []
        for path in paths:
            path_duration = self.get_path_duration(path)
            path_durations += [path_duration]

        # Find the shortest duration
        shortest_path_duration = path_durations[0]
        shortest_path = paths[0]
        if len(paths) > 1:
            for i in range(1, len(paths)):
                if path_durations[i] < shortest_path_duration:
                    shortest_path_duration = path_durations[i]
                    shortest_path = paths[i]
        return shortest_path

    # Obtain all flight numbers and destination airports from flights table based on origin airport
    def get_flights_from_airport(self, airport):

        # Connect the database and create a cursor
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

        # Obtain all Flight_Number and To_Airport from Flights table based on From_Airport
        self.c.execute(Q.select_flights_from_airport, (airport,))
        attached_airports = self.c.fetchall()

        # Close database connection
        self.conn.close()

        return attached_airports

    # Determine if the first flight will arrive before the last flight departs
    def is_later(self, first, last):

        # Connect the database and create a cursor
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

        # If the previous flight is None, every flight is later
        if first is None:
            self.conn.close()
            return True

        # Determine arrival time of the first flight
        self.c.execute(Q.select_arrival_from_flight, (first,))
        first_arrival = self.convert_to_time((self.c.fetchall()[0])[0])

        # Determine departure time of the last flight
        self.c.execute(Q.select_depart_from_flight, (last,))
        last_depart = self.convert_to_time((self.c.fetchall()[0])[0])

        # CLose database connection
        if first_arrival < last_depart:
            self.conn.close()
            return True
        else:
            self.conn.close()
            return False

    def get_path_duration(self, path):

        # Connect the database and create a cursor
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

        duration = 0.0
        previous_arrival = None
        for i in range(2, len(path), 2):

            # Determine departure time of first flight
            self.c.execute(Q.select_depart_from_flight, (path[i],))
            flight_depart = self.convert_to_time((self.c.fetchall()[0])[0])
            date_depart = datetime(2000, 1, 1, flight_depart.hour, flight_depart.minute, flight_depart.second)

            # Determine arrival time of last flight
            self.c.execute(Q.select_arrival_from_flight, (path[i],))
            flight_arrival = self.convert_to_time((self.c.fetchall()[0])[0])
            date_arrival = datetime(2000, 1, 1, flight_arrival.hour, flight_arrival.minute, flight_arrival.second)

            # Add duration of flight to duration
            duration += (date_arrival - date_depart).total_seconds()

            # If there is a previous flight, add the layover time
            if previous_arrival is not None:
                date_previous = datetime(2000, 1, 1, previous_arrival.hour, previous_arrival.minute, previous_arrival.second)
                if previous_arrival < flight_depart:
                    duration += (date_depart - date_previous).total_seconds()
                else:
                    duration += 24*60*60 - (date_depart - date_previous).total_seconds()

            previous_arrival = flight_arrival

        # CLose database connection
        self.conn.close()

        return duration

    # Converts a string to a time
    def convert_to_time(self, string):
        return datetime.strptime(string, '%H:%M:%S').time()

    def get_airports(self):
        # Connect the database and create a cursor
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

        # Obtain all Flight_Number and To_Airport from Flights table based on From_Airport
        self.c.execute(Q.select_airport_list)
        original_airports = self.c.fetchall()

        # Convert list of tuples to list
        airports = []
        for i in range(len(original_airports)):
            airports.append((original_airports[i])[0])

        # Close database connection
        self.conn.close()

        return airports
