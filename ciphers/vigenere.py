#!/usr/bin/env python

""" Vigenere cipher """
import argparse
import string
import re
import sys

""" Get a character from an alphabetline. """
def get_index(alphabet, keychar):
    try:
        return alphabet.index(keychar)
    except ValueError as e:
        print('ValueError: Could not find ' + keychar + ' from:')
        print(alphabet)
        print('Check the alphabet.')
        sys.exit(1)

""" Get the relevant line from Vigenere square """
def get_alphabet_line(row, alphabet=string.ascii_uppercase):
    line = []
    # Create alphabet line
    for i in range(len(alphabet)):
        shift = i + row
        if shift >= len(alphabet):
            shift -= len(alphabet)
        line.append(alphabet[shift])
    return line

""" Get encrypted char from Vigenere square """
def get_char_from_square(plainchar, keychar, alphabet):
    column = get_index(alphabet, plainchar)
    row = get_index(alphabet, keychar)
    alphabetline = get_alphabet_line(row, alphabet)
    return alphabetline[column]

""" Get a plaintext char from Vigenere square  """
def get_label_from_square(plainchar, keychar, alphabet):
    row = get_index(alphabet, keychar)
    alphabetline = get_alphabet_line(row, alphabet)
    return alphabet[alphabetline.index(plainchar)]

""" General Vigenere """
def morph_vigenere(text, key, morph_function, alphabet=''):
    a = string.ascii_uppercase
    morphtext = []
    if alphabet:
        alphabet = regex_to_string(alphabet)
    else:
        text = text.upper()
        key = key.upper()
        alphabet = string.ascii_uppercase
    i = 0
    for c in text:
        try:
            key[i]
        except:
            i = 0
        if c not in alphabet:
            morphtext.append(c)
        else:
            morphtext.append(morph_function(c, key[i], alphabet))
            i += 1
    return ''.join(morphtext)

""" Encryption """
def encrypt_vigenere(plaintext, key, alphabet=''):
    return morph_vigenere(plaintext, key, get_char_from_square, alphabet)

""" Decryption """
def decrypt_vigenere(ciphertext, key, alphabet=''):
    return morph_vigenere(ciphertext, key, get_label_from_square, alphabet)

""" Parse input regex alphabet to a string """
def regex_to_string(regex):
    alphabet = ''
    allchars = string.ascii_lowercase + string.ascii_uppercase \
               + string.digits + string.punctuation
    for c in allchars:
        if re.search(regex, c):
            alphabet += c
    return alphabet

""" Main """
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt and decrypt Vigenere cipher.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--encrypt', action='store_true', help='Encrypt Vigenere cipher.')
    group.add_argument('-d', '--decrypt', action='store_true', help='Decrypt Vigenere cipher.')
    parser.add_argument('key', help='Keyword you want to use to encrypt/decrypt a string.')
    parser.add_argument('input', help='String that you want to encrypt/decrypt.')
    parser.add_argument('-a', '--alphabet', help='Alphabet to use. E.g. [a-zA-Z{}]')
    args = parser.parse_args()
    
    if args.encrypt:
        print(encrypt_vigenere(args.input, args.key, args.alphabet))
    elif args.decrypt:
        print(decrypt_vigenere(args.input, args.key, args.alphabet))
