#!/usr/bin/env python3.6
import argparse
import json

def createParser():
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

def encode_caesar(args):
	input_string = search_file(args.input_file)
	Up_register_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	Lower_register_letter = "abcdefghijklmnopqrstuvwxyz"
	length = len(input_string)
	output_string = str()
	for i in range(length):
		letter = input_string[i]
		if (Lower_register_letter.find(letter.lower())) == -1:
			output_string += letter
		elif (Lower_register_letter.find(letter)) != -1:
			i = Lower_register_letter.find(letter)
			was_Lower_letter = True
		else:
			i = Up_register_letter.find(letter)
			was_Lower_letter = False
		if (Lower_register_letter.find(letter.lower())) != -1:
			new_i = (i + int(args.key)) % 26
			if (was_Lower_letter == True):
				output_string += Lower_register_letter[new_i]
			else:
				output_string += Up_register_letter[new_i]
	return output_string
			

def decode_caesar(args, string):
	if (string == ''):
		input_string = search_file(args.input_file)
	else:
		input_string = string
	Up_register_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	Lower_register_letter = "abcdefghijklmnopqrstuvwxyz"
	length = len(input_string)
	output_string = str()
	for i in range(length):
		letter = input_string[i]
		if (Lower_register_letter.find(letter.lower())) == -1:
			output_string += letter
		elif (Lower_register_letter.find(letter)) != -1:
			i = Lower_register_letter.find(letter)
			was_Lower_letter = True
		else:
			i = Up_register_letter.find(letter)
			was_Lower_letter = False
		if (Lower_register_letter.find(letter.lower())) != -1:
			new_i = (i - int(args.key)) % 26
			if (was_Lower_letter == True):
				output_string += Lower_register_letter[new_i]
			else:
				output_string += Up_register_letter[new_i]
	return output_string

def encode_vigenere(args):
	input_string = search_file(args.input_file)
	length_input_string = len(input_string)
	#Up_register_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	Lower_register_letter = "abcdefghijklmnopqrstuvwxyz"
	#for i in range(length_input_string):
		#if (Lower_register_letter.find(input_string[i].lower()) != -1):
			#string_only_letter += input_string[i]
	k = 0
	output_string = str()
	length_key = len(args.key)
	for i in range(length_input_string):
		if (Lower_register_letter.find(input_string[i].lower()) == -1):
			output_string += input_string[i]
		else:
			if (input_string[i].islower() == True):
				was_is_letter_lower_register = True
			else:
				was_is_letter_lower_register = False
			j = Lower_register_letter.find(input_string[i].lower())
			j_key = Lower_register_letter.find(args.key[k % length_key].lower())
			new_j = (j + j_key) % 26
			if (was_is_letter_lower_register == True):
				output_string += Lower_register_letter[new_j]
			else:
				output_string += Lower_register_letter[new_j].upper()
			k += 1
	return output_string

def decode_vigenere(args):
	input_string = search_file(args.input_file)
	length_input_string = len(input_string)
	#Up_register_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	Lower_register_letter = "abcdefghijklmnopqrstuvwxyz"
	#for i in range(length_input_string):
		#if (Lower_register_letter.find(input_string[i].lower()) != -1):
			#string_only_letter += input_string[i]
	k = 0
	output_string = str()
	length_key = len(args.key)
	for i in range(length_input_string):
		if (Lower_register_letter.find(input_string[i].lower()) == -1):
			output_string += input_string[i]
		else:
			if (input_string[i].islower() == True):
				was_is_letter_lower_register = True
			else:
				was_is_letter_lower_register = False
			j = Lower_register_letter.find(input_string[i].lower())
			j_key = Lower_register_letter.find(args.key[k % length_key].lower())
			new_j = (j - j_key) % 26
			if (was_is_letter_lower_register == True):
				output_string += Lower_register_letter[new_j]
			else:
				output_string += Lower_register_letter[new_j].upper()
			k += 1
	return output_string

def train_file(args):
	input_string = search_file(args.text_file)
	d = {}
	d = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
	Lower_register_letter = "abcdefghijklmnopqrstuvwxyz"
	length_input_string = len(input_string)
	for i in range(length_input_string):
		if (Lower_register_letter.find(input_string[i].lower()) != -1):
			d[input_string[i].lower()] += 1
	json_string = json.dumps(d)
	return json_string

def search_letter(output_string):
	d = {}
	d = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
	Lower_register_letter = "abcdefghijklmnopqrstuvwxyz"
	length_output_string = len(output_string)
	for i in range(length_output_string):
		if (Lower_register_letter.find(output_string[i].lower()) != -1):
			d[output_string[i].lower()] += 1
	return d

def search_rating_key(rating_key, dict_key, model_dict):
	Lower_register_letter = "abcdefghijklmnopqrstuvwxyz"
	result = 0
	for i in range(26):
		result += (model_dict[Lower_register_letter[i]] - dict_key[Lower_register_letter[i]]) ** 2
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
	for i in range(1, 26):
		if (rating_key[i] < min_rating):
			min_rating = rating_key[i]
			k = i
	args.key = str(k)	
	output_string = decode_caesar(args, input_string)
	return output_string	
	

parser = createParser()
args = parser.parse_args()
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
print(args)





