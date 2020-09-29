"""
Created on September 12, 2020
Author: Richard Punt
Version: Python 3.8
Description: Executes Graph class

"""

import sys
from PyQt5.Qt import *
from pathlib import Path
from Graph import *


class FlightPathWidget(QWidget):

    def __init__(self):

        # Inherit QWidget properties and initiate the program
        super(FlightPathWidget, self).__init__()
        self.initUI()

    def initUI(self):

        # Create an instance of the graph class
        file_path = Path('C:/Users/Richa/Desktop/Python/Assignment 6/Input/RawData_update3.xlsx')
        self.g = Graph(file_path, 'Graph.db')

        # Window properties
        self.resize(585, 420)
        self.setWindowTitle('Flight Path Widget')
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

        # Widget properties
        self.label_departure = QLabel('Departure:', self)
        self.combo_box_departure = QComboBox(self)
        self.combo_box_departure.addItem("")
        self.combo_box_departure.addItems(self.g.get_airports())
        self.label_destination = QLabel('Destination:', self)
        self.combo_box_destination = QComboBox(self)
        self.combo_box_destination.addItem("")
        self.combo_box_destination.addItems(self.g.get_airports())
        self.button_search = QPushButton('Search', self)
        self.button_search.clicked.connect(self.search_paths)
        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)
        self.button_reset_view = QPushButton('Reset View', self)
        self.button_reset_view.clicked.connect(self.text_output.clear)
        self.insert_blank_line = QLabel('', self)

        # Layout properties
        self.layout = QGridLayout()
        self.layout.addWidget(self.label_departure, 0, 0, 1, 1)
        self.layout.addWidget(self.combo_box_departure, 0, 1, 1, 3)
        self.layout.addWidget(self.label_destination, 1, 0, 1, 1)
        self.layout.addWidget(self.combo_box_destination, 1, 1, 1, 3)
        self.layout.addWidget(self.insert_blank_line, 2, 0, 1, 1)
        self.layout.addWidget(self.button_search, 3, 3, 1, 4)
        self.layout.addWidget(self.insert_blank_line, 4, 0, 1, 1)
        self.layout.addWidget(self.text_output, 5, 0, 1, 10)
        self.layout.addWidget(self.insert_blank_line, 6, 0, 1, 1)
        self.layout.addWidget(self.button_reset_view, 7, 3, 1, 4)
        self.layout.addWidget(self.insert_blank_line, 8, 0, 1, 1)
        self.setLayout(self.layout)

        # Show application
        self.show()

    def search_paths(self):

        # Clear existing text output
        self.text_output.clear()

        # Determine current combo box departure and destination
        departure = self.combo_box_departure.currentText()
        destination = self.combo_box_destination.currentText()

        # Test if combo boxes not filled out or if destination and departure are the same
        if departure == "" or destination == "":
            self.text_output.insertPlainText("Not applicable destination or departure")
        elif departure == destination:
            self.text_output.insertPlainText("Departure and destination cannot be the same")
        else:

            # Obtain paths for departure and destination
            paths = self.g.find_paths(departure, destination, departure)

            # Check if no paths exist
            if paths == []:
                self.text_output.insertPlainText("No paths exist")
            else:

                # Print out each path
                for path in paths:
                    path_string = "Path: " + path[1]
                    for i in range(2, len(path)):
                        if i % 2 == 0:
                            path_string += " to " + path[i + 1] + " via " + path[i]
                    self.text_output.insertPlainText(path_string + "\n")

                # Print out shortest path
                shortest_path = self.g.find_shortest_path(departure, destination)
                shortest_path_string = "\nThe shortest path is " + shortest_path[1]
                for i in range(2, len(shortest_path)):
                    if i % 2 == 0:
                        shortest_path_string += " to " + shortest_path[i + 1] + " via " + shortest_path[i]
                self.text_output.insertPlainText(shortest_path_string + ".")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = FlightPathWidget()
    sys.exit(app.exec_())



