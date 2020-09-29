"""
Created on September 14, 2020
Author: Richard Punt
Version: Python 3.8

"""
import random


class Crypto(object):

    def __init__(self):

        # Primary and Secondary keys
        self.key = []
        self.key2 = []

    def set_key(self, key):

        # Convert 8 bit hex string to four 2 bit hex strings in a list
        self.key = [int(key[0:2], 16), int(key[2:4], 16), int(key[4:6], 16), int(key[6:8], 16)]

        # Generate binary mirrored key => convert hext key to binary, pad to 32 , reverse it, convert to hex, pad to 8
        key_bin = bin(int(key, 16))[2:]
        while len(key_bin) < 32:
            key_bin = "0" + key_bin
        bin_mir = key_bin[::-1]
        key_mir = hex(int(bin_mir, 2))[2:]
        while len(key_mir) > 8:
            key_mir = "0" + key_mir
        self.key2 = [int(key_mir[0:2], 16), int(key_mir[2:4], 16), int(key_mir[4:6], 16), int(key_mir[6:8], 16)]

    def generate_key(self, binary_key=None):

        # Generate random 8 digit hex key
        # If binary key provided, convert it to 8 digit hex key
        if binary_key is None:
            key = ""
            for i in range(32):
                key += str(random.randint(0, 1))
            hex_key = hex(int(key, 2))[2:]
        else:
            hex_key = hex(int(binary_key, 2))[2:]
        while len(hex_key) > 8:
            hex_key = "0" + hex_key
        return hex_key

    def encode(self, decoded_text):

        encoded_text = ""
        decoded_length = len(decoded_text)
        bytes_length = int(decoded_length / 4)
        extra_bits = decoded_length % 4

        # For each packet of 4 characters, use ord(x) to compare to the primary and secondary keys with XOR
        # Convert to hex string and join to form encoded text
        for i in range(bytes_length):
            byte = decoded_text[4 * i:4 * (i + 1)]
            byte_div = [byte[0], byte[1], byte[2], byte[3]]
            for j in range(4):
                byte_div[j] = ord(byte_div[j])
                byte_div[j] = byte_div[j] ^ self.key[j] ^ self.key2[j]
                byte_div[j] = hex(byte_div[j])[2:]
                while len(byte_div[j]) < 2:
                    byte_div[j] = "0" + byte_div[j]
            encoded_text = encoded_text + ''.join(byte_div)

        # Repeat for last set of characters that have less that 4 elements
        for k in range(extra_bits):
            bit = decoded_text[decoded_length - extra_bits + k]
            bit_num = ord(bit) ^ self.key[k] ^ self.key2[k]
            bit_num = hex(bit_num)[2:]
            while len(bit_num) < 2:
                bit_num = "0" + bit_num
            encoded_text = encoded_text + bit_num
        return encoded_text

    def decode(self, encoded_text):

        decoded_text = ""
        encoded_length = len(encoded_text)
        bytes_length = int(encoded_length/8)
        extra_bits = encoded_length % 8

        # For each packet of 8 hex digits, use int(x) to compare to the primary and secondary keys with XOR
        # Convert to chr and join to form decoded text
        for i in range(bytes_length):
            byte = encoded_text[8*i:8*(i+1)]
            for j in range(4):
                bit = byte[2*j:2*(j+1)]
                bit_num = int(bit, 16) ^ self.key[j] ^ self.key2[j]
                decoded_text = decoded_text + chr(bit_num)

        # Repeat for last set of characters that have less that 8 elements
        for k in range(int(extra_bits/2)):
            bit = encoded_text[encoded_length - extra_bits + 2*k:encoded_length - extra_bits + 2*(k+1)]
            bit_num = int(bit, 16) ^ self.key[k] ^ self.key2[k]
            decoded_text = decoded_text + chr(bit_num)
        return decoded_text
