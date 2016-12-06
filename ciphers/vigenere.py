#!/usr/bin/env python
""" Vigenere cipher """
import argparse
import string

""" Helper functions """
def get_alphabet_line(row):
    line = []
    # Create alphabet line
    for i in range(len(string.ascii_uppercase)):
        shift = i + row
        if shift >= len(string.ascii_uppercase):
            shift -= len(string.ascii_uppercase)
        line.append(string.ascii_uppercase[shift])
    return line

def get_char_from_square(plainchar, keychar):
    column = string.ascii_uppercase.index(plainchar)
    row = string.ascii_uppercase.index(keychar)
    alphabet = get_alphabet_line(row)
    return alphabet[column]

def get_label_from_square(plainchar, keychar):
    row = string.ascii_uppercase.index(keychar)
    alphabet = get_alphabet_line(row)
    return string.ascii_uppercase[alphabet.index(plainchar)]
    
""" Vigenere """
def morph_vigenere(text, key, morph_function):
    text = text.upper()
    morphtext = []
    i = 0
    for c in text:
        try:
            key[i]
        except:
            i = 0
        if c not in string.ascii_uppercase:
            morphtext.append(c)
        else:
            morphtext.append(morph_function(c, key[i]))
            i += 1
    return ''.join(morphtext)
    
""" Encryption """
def encrypt_vigenere(plaintext, key):
    return morph_vigenere(plaintext, key, get_char_from_square)

""" Decryption """
def decrypt_vigenere(ciphertext, key):
    return morph_vigenere(ciphertext, key, get_label_from_square)

""" Main """
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encrypt and decrypt Vigenere cipher.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--encrypt', action='store_true', help='Encrypt Vigenere cipher.')
    group.add_argument('-d', '--decrypt', action='store_true', help='Decrypt Vigenere cipher.')
    parser.add_argument('key', help='Keyword you want to use to encrypt/decrypt a string.')
    parser.add_argument('input', help='String that you want to encrypt/decrypt.')
    args = parser.parse_args()
    
    if args.encrypt:
        print(encrypt_vigenere(args.input, args.key))
    elif args.decrypt:
        print(decrypt_vigenere(args.input, args.key))
