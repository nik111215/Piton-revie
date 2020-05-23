#!/usr/bin/env python3.6
import argparse
import json
import string


LOWER_REGISTER_LETTER = string.ascii_lowercase
UP_REGISTER_LETTER = string.ascii_uppercase
ALPHABET_SIZE = len(string.ascii_lowercase)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type = str)
    parser.add_argument('--cipher', default = None, type = str)
    parser.add_argument("--key", default = None, type = str)
    parser.add_argument("--input-file", default = None, type = str)
    parser.add_argument("--output-file", default = None, type = str)
    parser.add_argument('--text-file', default = None, type = str)
    parser.add_argument('--model-file', default = None, type = str)	
    return parser


def search_file(name_file):
    if name_file == None:
        input_string = input()
    else:
        with open(name_file,'r') as file_reading:	
            input_string= ''.join(line for line in file_reading)
    return input_string


def search_output_file(name_output_file, output_string):
    if name_output_file != None:
        with open(name_output_file, 'w') as file_writting:
            file_writting.write(output_string)
    else:
        print(output_string)


def encode_or_decode_caesar(args, input_string, is_encode_caesar):
    output_string = ""
    index = -1
    l = []
    for i, letter in enumerate(input_string):
        was_lower_letter = letter.islower()
        if LOWER_REGISTER_LETTER.find(letter.lower()) == -1:
            l += str(letter)
        if LOWER_REGISTER_LETTER.find(letter.lower()) != -1:
            index = LOWER_REGISTER_LETTER.find(letter.lower())
        if index != -1:
            if is_encode_caesar:
                new_i = (index + int(args.key)) % ALPHABET_SIZE	
            else:
                new_i = (index - int(args.key)) % ALPHABET_SIZE
        if was_lower_letter:
            l += LOWER_REGISTER_LETTER[new_i]
        else:
            l += LOWER_REGISTER_LETTER[new_i].upper()
    output_string = ''.join(l)
    return output_string


def encode_caesar(args):
    input_string = search_file(args.input_file)
    output_string = encode_or_decode_caesar(args, input_string, is_encode_caesar = True)
    return output_string
			

def decode_caesar(args, string):
    if string == None:
        input_string = search_file(args.input_file)
    else:
        input_string = string
    output_string = encode_or_decode_caesar(args, input_string, is_encode_caesar = False)
    return output_string


def encode_or_decode_vigenere(args, is_encode_vigenere):
    input_string = search_file(args.input_file)
    length_input_string = len(input_string)
    k = 0
    output_string = ""
    l = []
    length_key = len(args.key)
    for i in range(length_input_string):
        if LOWER_REGISTER_LETTER.find(input_string[i].lower()) == -1:
            l += str(input_string[i])
        else:
            was_is_letter_lower_register = input_string[i].islower();
            j = LOWER_REGISTER_LETTER.find(input_string[i].lower())
            j_key = LOWER_REGISTER_LETTER.find(args.key[k % length_key].lower())
            if is_encode_vigenere:
                new_j = (j + j_key) % ALPHABET_SIZE
            else:
                new_j = (j - j_key) % ALPHABET_SIZE
            if was_is_letter_lower_register:
                l += LOWER_REGISTER_LETTER[new_j]
            else:
                l += LOWER_REGISTER_LETTER[new_j].upper()
            k += 1
    output_string = ''.join(l)
    return output_string


#def decode_vigenere(args):
#    input_string = search_file(args.input_file)
#    length_input_string = len(input_string)
#    k = 0
 #   output_string = ""
  #  l = []
   # length_key = len(args.key)
    #for i in range(length_input_string):
#        if LOWER_REGISTER_LETTER.find(input_string[i].lower()) == -1:
 #           l += str(input_string[i])
  #      else:
   #         was_is_letter_lower_register = input_string[i].islower()
    #        j = LOWER_REGISTER_LETTER.find(input_string[i].lower())
     #       j_key = LOWER_REGISTER_LETTER.find(args.key[k % length_key].lower())
      #      new_j = (j - j_key) % ALPHABET_SIZE
       #     if was_is_letter_lower_register:
        #        l += LOWER_REGISTER_LETTER[new_j]
         #   else:
          #      l += LOWER_REGISTER_LETTER[new_j].upper()
           # k += 1
#    output_string = ''.join(l)
 #   return output_string


def train_file(args):
    input_string = search_file(args.text_file)
    length_lower_register_letter = len(LOWER_REGISTER_LETTER)
    d = {letter	: 0 for letter in LOWER_REGISTER_LETTER}
    length_input_string = len(input_string)
    for i in range(length_input_string):
        if LOWER_REGISTER_LETTER.find(input_string[i].lower()) != -1:
            d[input_string[i].lower()] += 1
    return json.dumps(d)


def search_letter(output_string):
    length_lower_register_letter = len(LOWER_REGISTER_LETTER)
    d = {LOWER_REGISTER_LETTER[i]: 0 for i in range(length_lower_register_letter)}
    length_output_string = len(output_string)
    for i in range(length_output_string):
        if LOWER_REGISTER_LETTER.find(output_string[i].lower()) != -1:
            d[output_string[i].lower()] += 1
    return d


def search_rating_key(rating_key, dict_key, model_dict, ofset):
    result = 0
    for i in range(ALPHABET_SIZE):
        result += (model_dict[LOWER_REGISTER_LETTER[i + ofset]] - dict_key[LOWER_REGISTER_LETTER[i]]) ** 2
    rating_key.append(result)
    return rating_key


def hack_cipher_caesar(args):
    input_string = search_file(args.input_file)
    with open(args.model_file, 'r') as json_file:
        model_dict = json.load(json_file)
    rating_key = []
    args.key = str(i)	
    output_string = decode_caesar(args, input_string)
    dict_key = search_letter(output_string)
    rating_key = search_rating_key(rating_key, dict_key, model_dict, ofset = 0)
    for i in range(2, ALPHABET_SIZE + 1):
        rating_key = search_rating_key(rating_key, dict_key, model_dict, ofset = i)
    min_rating = rating_key[0]
    k = 0
    for i in range(1, ALPHABET_SIZE):
        if rating_key[i] < min_rating:
            min_rating = rating_key[i]
            k = i
    args.key = str(k)	
    output_string = decode_caesar(args, input_string)
    return output_string	


def encode_or_decode_vermana(args):
    input_string = search_file(args.input_file)
    length_input_string = len(input_string)
    result_string = None
    l = []
    for i in range(length_input_string):
        symbol_input_string = input_string[i]
        symbol_key = args.key[i]
        int_symbol_input_string = ord(symbol_input_string) 		
        int_symbol_key = ord(symbol_key)
        result_symbol = int_symbol_input_string ^ int_symbol_key 
        l += str(chr(result_symbol))
    result_string = ''.join(l)
    return result_string


parser = create_parser()
args = parser.parse_args()
if args.mode == 'encode':
    if args.cipher == 'caesar':
        output_string = encode_caesar(args)
    elif args.cipher == 'vigenere':
        output_string = encode_or_decode_vigenere(args, is_encode_vigenere = True)
    else:
        output_string = encode_or_decode_vermana(args)
if args.mode == 'decode':
    if args.cipher == 'caesar':
        output_string = decode_caesar(args, '')
    elif rgs.cipher == 'vigenere':
        output_string = encode_or_decode_vigenere(args, is_encode_vigenere = False)
    else:
        output_string = encode_or_decode_vermana(args)
search_output_file(args.output_file, output_string)
if args.mode == 'train':
    json_string = train_file(args)
    search_output_file(args.model_file, json_string)
if args.mode == 'hack':
    output_string = hack_cipher_caesar(args)
    search_output_file(args.output_file, output_string)        

