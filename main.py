"""
Created on September 12, 2020
Author: Richard Punt
Version: Python 3.8

"""
import sys
from PyQt5.Qt import *
from Crypto import *
from itertools import *


class CryptoWidget(QWidget):

    # Constructor
    def __init__(self):
        # Inherit QWidget properties and initiate the program
        super(CryptoWidget, self).__init__()
        self.initUI()

    def initUI(self):
        # Create an instance of the Crypto class
        self.c = Crypto()

        # Window properties
        self.resize(970, 580)
        self.setWindowTitle('Crypto Tool')
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())

        # Widget properties
        self.label_key_file = QLabel('Key File', self)
        self.button_key_file_generate = QPushButton('Generate', self)
        self.button_key_file_generate.clicked.connect(self.generate_key_file)
        self.text_line_key_file = QLineEdit(self)
        self.text_line_key_file.setReadOnly(True)
        self.text_line_key_file.selectionChanged.connect(lambda: self.text_line_key_file.setSelection(0, 0))
        self.button_key_file_browse = QPushButton('Browse', self)
        self.button_key_file_browse.clicked.connect(self.get_key_file)
        self.label_source_file = QLabel('Source File', self)
        self.text_line_source_file = QLineEdit(self)
        self.button_source_file_browse = QPushButton('Browse', self)
        self.button_source_file_browse.clicked.connect(self.get_source_file)
        self.insert_blank_line = QLabel('', self)
        self.insert_blank_line.setFont(QFont('Arial', 5))
        self.button_encode = QPushButton('Encode', self)
        self.button_encode.clicked.connect(self.encode)
        self.button_decode = QPushButton('Decode', self)
        self.button_decode.clicked.connect(self.decode)
        self.text_line_key = QLineEdit(self)
        self.text_line_key.setReadOnly(True)
        self.text_line_key.selectionChanged.connect(lambda: self.text_line_key.setSelection(0, 0))
        self.text_line_input_text = QLineEdit('Input Text', self)
        self.text_line_input_text.setReadOnly(True)
        self.text_line_input_text.selectionChanged.connect(lambda: self.text_line_input_text.setSelection(0, 0))
        self.text_input_text = QTextEdit(self)
        self.text_input_text.setReadOnly(True)
        self.text_line_output_text = QLineEdit('Output Text', self)
        self.text_line_output_text.setReadOnly(True)
        self.text_line_output_text.selectionChanged.connect(lambda: self.text_line_output_text.setSelection(0, 0))
        self.text_output_text = QTextEdit(self)
        self.text_output_text.setReadOnly(True)

        # Layout properties
        self.layout = QGridLayout()
        self.layout.addWidget(self.label_key_file, 0, 0, 1, 2)
        self.layout.addWidget(self.button_key_file_generate, 0, 2, 1, 1)
        self.layout.addWidget(self.text_line_key_file, 0, 3, 1, 6)
        self.layout.addWidget(self.button_key_file_browse, 0, 9, 1, 1)
        self.layout.addWidget(self.label_source_file, 1, 0, 1, 3)
        self.layout.addWidget(self.text_line_source_file, 1, 3, 1, 6)
        self.layout.addWidget(self.button_source_file_browse, 1, 9, 1, 1)
        self.layout.addWidget(self.insert_blank_line, 2, 0, 1, 5)
        self.layout.addWidget(self.button_encode, 3, 0, 1, 5)
        self.layout.addWidget(self.button_decode, 3, 5, 1, 5)
        self.layout.addWidget(self.insert_blank_line, 4, 0, 1, 5)
        self.layout.addWidget(self.text_line_key, 5, 0, 1, 10)
        self.layout.addWidget(self.text_line_input_text, 6, 0, 1, 10)
        self.layout.addWidget(self.text_input_text, 7, 0, 1, 10)
        self.layout.addWidget(self.text_line_output_text, 8, 0, 1, 10)
        self.layout.addWidget(self.text_output_text, 9, 0, 1, 10)
        self.setLayout(self.layout)

        # Show application
        self.show()

    def generate_key_file(self):
        # Generate and set hex_key
        hex_key = self.c.generate_key()
        self.c.set_key(hex_key)

        # Create My_Key.txt to put hex_key in
        f = open("My_Key.txt", "w+")
        f.write(hex_key)
        f.close()

        # Display key and key file path
        self.text_line_key.setText("Key: " + hex_key)
        self.text_line_key_file.setText('C:\\Users\\Richa\\Desktop\\Python\\Final Project\\My_Key.txt')

    def get_key_file(self):
        # Browse for key file
        key_file_name = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\Users\\Richa\\Desktop\\Python\\Final Project', "Text files (*.txt)")
        self.text_line_key_file.setText(key_file_name[0])

        # Display key and key file path and set hex_key
        try:
            key_file = open(key_file_name[0], 'r')
            with key_file:
                hex_key = key_file.read()
                self.text_line_key.setText("Key: " + hex_key)
            self.c.set_key(hex_key)
        except FileNotFoundError:
            pass

    def get_source_file(self):
        # Browse for source file
        get_source_file = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\Users\\Richa\\Desktop\\Python\\Final Project', "Text files (*.txt) ;; Enc files (*.enc)")
        self.text_line_source_file.setText(get_source_file[0])

        # Display source text
        try:
            self.text_input_text.clear()
            self.text_output_text.clear()
            key_file = open(get_source_file[0], 'r')
            with key_file:
                data = key_file.read()
                self.text_input_text.setText(data)
        except FileNotFoundError:
            pass

    def encode(self):
        # Split input text into a list by \n
        text = self.text_input_text.toPlainText().split('\n')

        # Encode each line and display in output text
        for line in text:
            encrypt = self.c.encode(line)
            self.text_output_text.append(encrypt.strip())

    def decode(self):
        # Split input text into a list
        text = self.text_input_text.toPlainText().split()

        # Decode each line and display in output text
        for line in text:
            decrypt = self.c.decode(line)
            print(decrypt)
            self.text_output_text.append(decrypt.strip())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CryptoWidget()
    sys.exit(app.exec_())
