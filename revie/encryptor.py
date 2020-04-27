#!/usr/bin/env python3.6
import argparse
import json
import string

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type = str)
    parser.add_argument('--cipher', default = '', type = str)
    parser.add_argument("--key", default = '', type = str)
    parser.add_argument("--input-file", default = '', type = str)
    parser.add_argument("--output-file", default = '', type = str)
    parser.add_argument('--text-file', default = '', type = str)
    parser.add_argument('--model-file', default = '', type = str)
	
    return parser

def search_file(name_file):
    if (name_file == ''):
        input_string = input()
    else:
        with open(name_file,'r') as file_reading:	
            input_string= ''.join(line for line in file_reading)
    return input_string

def search_output_file(name_output_file, output_string):
    if (name_output_file != ''):
        with open(name_output_file, 'w') as file_writting:
            file_writting.write(output_string)
    else:
        print(output_string)

def encode_or_decode_caesar(args, input_string, is_encode_caesar):
    length = len(input_string)
    output_string = str()
    for i in range(length):
        letter = input_string[i]
        if (LOWER_REGISTER_LETTER.find(letter.lower())) == -1:
            output_string += letter
        elif (LOWER_REGISTER_LETTER.find(letter)) != -1:
            i = LOWER_REGISTER_LETTER.find(letter)
            was_Lower_letter = True
        else:
            i = UP_REGISTER_LETTER.find(letter)
            was_Lower_letter = False
        if (LOWER_REGISTER_LETTER.find(letter.lower())) != -1:
            if (is_encode_caesar == True):
                new_i = (i + int(args.key)) % size
            else:
                new_i = (i - int(args.key)) % size
            if (was_Lower_letter == True):
                output_string += LOWER_REGISTER_LETTER[new_i]
            else:
                output_string += UP_REGISTER_LETTER[new_i]
    return output_string

def encode_caesar(args):
    input_string = search_file(args.input_file)
    is_encode_caesar = True
    output_string = encode_or_decode_caesar(args, input_string, is_encode_caesar)
    return output_string
			

def decode_caesar(args, string):
    if (string == ''):
        input_string = search_file(args.input_file)
    else:
        input_string = string
    is_encode_caesar = False
    output_string = encode_or_decode_caesar(args, input_string, is_encode_caesar)
    return output_string

def encode_vigenere(args):
    input_string = search_file(args.input_file)
    length_input_string = len(input_string)
    k = 0
    output_string = str()
    length_key = len(args.key)
    for i in range(length_input_string):
        if (LOWER_REGISTER_LETTER.find(input_string[i].lower()) == -1):
            output_string += input_string[i]
        else:
            if (input_string[i].islower() == True):
                was_is_letter_lower_register = True
            else:
                was_is_letter_lower_register = False
            j = LOWER_REGISTER_LETTER.find(input_string[i].lower())
            j_key = LOWER_REGISTER_LETTER.find(args.key[k % length_key].lower())
            new_j = (j + j_key) % size
            if (was_is_letter_lower_register == True):
                output_string += LOWER_REGISTER_LETTER[new_j]
            else:
                output_string += LOWER_REGISTER_LETTER[new_j].upper()
            k += 1
    return output_string

def decode_vigenere(args):
    input_string = search_file(args.input_file)
    length_input_string = len(input_string)
    k = 0
    output_string = str()
    length_key = len(args.key)
    for i in range(length_input_string):
        if (LOWER_REGISTER_LETTER.find(input_string[i].lower()) == -1):
            output_string += input_string[i]
        else:
            if (input_string[i].islower() == True):
                was_is_letter_lower_register = True
            else:
                was_is_letter_lower_register = False
            j = LOWER_REGISTER_LETTER.find(input_string[i].lower())
            j_key = LOWER_REGISTER_LETTER.find(args.key[k % length_key].lower())
            new_j = (j - j_key) % size
            if (was_is_letter_lower_register == True):
                output_string += LOWER_REGISTER_LETTER[new_j]
            else:
                output_string += LOWER_REGISTER_LETTER[new_j].upper()
            k += 1
    return output_string

def train_file(args):
    input_string = search_file(args.text_file)
    length_lower_register_letter = len(LOWER_REGISTER_LETTER)
    d = {LOWER_REGISTER_LETTER[i]: 0 for i in range(length_lower_register_letter)}
    length_input_string = len(input_string)
    for i in range(length_input_string):
        if (LOWER_REGISTER_LETTER.find(input_string[i].lower()) != -1):
            d[input_string[i].lower()] += 1
    json_string = json.dumps(d)
    return json_string

def search_letter(output_string):
    length_lower_register_letter = len(LOWER_REGISTER_LETTER)
    d = {LOWER_REGISTER_LETTER[i]: 0 for i in range(length_lower_register_letter)}
    length_output_string = len(output_string)
    for i in range(length_output_string):
        if (LOWER_REGISTER_LETTER.find(output_string[i].lower()) != -1):
            d[output_string[i].lower()] += 1
    return d

def search_rating_key(rating_key, dict_key, model_dict):
    result = 0
    for i in range(size):
        result += (model_dict[LOWER_REGISTER_LETTER[i]] - dict_key[LOWER_REGISTER_LETTER[i]]) ** 2
    rating_key.append(result)
    return rating_key


def hack_cipher_caesar(args):
    input_string = search_file(args.input_file)
    with open(args.model_file, 'r') as json_file:
        model_dict = json.load(json_file)
    rating_key = []
    for i in range(1, 27):
        args.key = str(i)	
        output_string = decode_caesar(args, input_string)
        dict_key = search_letter(output_string)
        rating_key = search_rating_key(rating_key, dict_key, model_dict)
    min_rating = rating_key[0]
    k = 0
    for i in range(1, size):
        if (rating_key[i] < min_rating):
            min_rating = rating_key[i]
            k = i
    args.key = str(k)	
    output_string = decode_caesar(args, input_string)
    return output_string	
	
#def search_symbol(symbol):
#    int_symbol = ord(symbol)
    

#def extension_max(binary_symbol_input_string, binary_symbol_key):
#    difference = len(binary_symbol_input_string) > len(binary_symbol_key)
#    if (difference > 0):
#        binary_symbol_key = '0' * difference + binary_symbol_key
#    else:
#        binary_symbol_input_string = '0' * abs(difference) + binary_symbol_input_string

#def getting_encrypt(binary_symbol_input_string, binary_symbol_key):
#    length = len(binary_symbol_key)
#    result = ''
#    for i in range(length):
#        result += str(int(binary_symbol_input_string) ^ int(binary_symbol_key))
#    result_letter = chr(int(result, 2))
#    return result_letter

def encode_or_decode_vermana(args):
    input_string = search_file(args.input_file)
    length_input_string = len(input_string)
    result_string = ''
    for i in range(length_input_string):
        symbol_input_string = input_string[i]
        symbol_key = args.key[i]
        int_symbol_input_string = ord(symbol_input_string) 		
        int_symbol_key = ord(symbol_key)
        result_symbol = int_symbol_input_string ^ int_symbol_key 
        result_string += chr(result_symbol)
    return result_string


parser = create_parser()
args = parser.parse_args()
LOWER_REGISTER_LETTER = string.ascii_lowercase
UP_REGISTER_LETTER = string.ascii_uppercase
size = 26
if (args.mode == 'encode' and args.cipher == 'caesar'):
    output_string = encode_caesar(args)
    search_output_file(args.output_file, output_string)
if (args.mode == 'decode' and args.cipher == 'caesar'):
    output_string = decode_caesar(args, '')
    search_output_file(args.output_file, output_string)
if (args.mode == 'encode' and args.cipher == 'vigenere'):
    output_string = encode_vigenere(args)
    search_output_file(args.output_file, output_string)
if (args.mode == 'decode' and args.cipher == 'vigenere'):
    output_string = decode_vigenere(args)
    search_output_file(args.output_file, output_string)
if (args.mode == 'train'):
    json_string = train_file(args)
    search_output_file(args.model_file, json_string)
if (args.mode == 'hack'):
    output_string = hack_cipher_caesar(args)
    search_output_file(args.output_file, output_string)
if (args.mode == 'encode' and args.cipher == 'vermana'):
    output_string = encode_or_decode_vermana(args)
    search_output_file(args.output_file, output_string)
if (args.mode == 'decode' and args.cipher == 'vermaan'):
    output_string = encode_or_decode_vermana(args)
    search_output_file(args,output_file, output_string)




