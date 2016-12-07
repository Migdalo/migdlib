""" Playfair cipher """

import argparse
import string

playfair_matrix = [['P', 'L', 'A', 'Y', 'F'], 
                   ['I', 'R', 'E', 'X', 'M'], 
                   ['B', 'C', 'D', 'G', 'H'], 
                   ['K', 'N', 'O', 'Q', 'S'], 
                   ['T', 'U', 'V', 'W', 'Z']]

''' Matrix '''
def get_new_pos(pos, shift_col, shift_row, playfair_matrix):
    try:
        return playfair_matrix[pos[0] + shift_col][pos[1] + shift_row]
    except IndexError as ie:
        if shift_col > 0: # Encode column
            return playfair_matrix[0][pos[1]]
        elif shift_col < 0: # Decode column
            return playfair_matrix[len(playfair_matrix)][pos[1]]
        elif shift_row > 0: # Encode row ->
            return playfair_matrix[pos[0]][0]
        elif shift_row < 0: # Decode row <-
            return playfair_matrix[pos[0]][len(playfair_matrix[pos[0]])]

def is_in_matrix(matrix, char):
    for line in matrix:
        if char in line: 
            return True
    return False

def create_matrix(key):
    linelen = 5
    keyidx = 0
    alphaidx = 0
    alphabet = string.ascii_uppercase
    key = key.upper()
    matrix = []
    for i in range(linelen):
        matrix.append([])
        for j in range(linelen):
            try:
                # Add a character from the key
                while is_in_matrix(matrix, key[keyidx]):
                    keyidx += 1
                matrix[i].append(key[keyidx])
                keyidx += 1
            except:
                # Add a character from alphabet
                try:
                    while is_in_matrix(matrix, alphabet[alphaidx]):
                        alphaidx += 1
                    matrix[i].append(alphabet[alphaidx])
                    alphaidx += 1
                except:
                    print('Failed to create a key matrix.')
                    return('')
    return matrix

""" Shift blocks """
def shift_block(char1, char2, matrix, shift_val):
    pos1 = (0, 0)
    pos2 = (0, 0)
    
    # Find the char position in playfair matrix
    for line in range(len(matrix)):
        if char1 in matrix[line]:
            pos1 = (line, matrix[line].index(char1))
        if char2 in matrix[line]:
            pos2 = (line, matrix[line].index(char2))
          
    if pos1[0] == pos2[0]: # Both chars on same line
        return get_new_pos(pos1, 0, shift_val, matrix) + get_new_pos(pos2, 0, -shift_val, matrix)
    elif pos1[1] == pos2[1]: # Both chars on same column
        return get_new_pos(pos1, shift_val, 0, matrix) + get_new_pos(pos2, shift_val, 0, matrix)
    else: # Square
        return matrix[pos1[0]][pos2[1]] + matrix[pos2[0]][pos1[1]]

""" Decrypt Playfair cipher """
def decode_playfair(cipherinput, key):
    global playfair_matrix
    results = ''
    if not key:
        matrix = playfair_matrix
    else:
        matrix = create_matrix(key)
    
    # Make sure the input is a list with two chars as elements
    cipher = cipherinput.upper().split()
    if len(cipher) == 1:
        cipher = []
        for i in range(0, len(cipherinput), 2):
            cipher.append(cipherinput[i:i+2])
            
    # Decode
    for tc in cipher:
        results += shift_block(tc[0], tc[1], matrix, -1)
    
    return results

""" Encrypt Playfair cipher """
def encode_playfair(plaintext, key):
    global playfair_matrix
    cipher = ''
    plaintext = list(''.join(plaintext.split()).upper())
    plain = []
    
    if not key:
        matrix = playfair_matrix
    else:
        matrix = create_matrix(key)
    
    # Handle double characters
    plaintext = handle_double_chars(plaintext)
    
    # Change the user input to be a list with two chars as elements
    for i in range(0, len(plaintext), 2):
        plain.append(''.join(plaintext[i:i+2]))
    
    # Encode
    for tc in plain:
        cipher += shift_block(tc[0], tc[1], matrix, 1)
    return cipher

""" 
If plaintext has two of the same chars next 
to each other, add x in between them. 
"""
def handle_double_chars(plaintext):
    counter = 0
    
    # Handle double characters
    while counter < len(plaintext) - 1:
        if plaintext[counter] == plaintext[counter + 1]:
            plaintext.insert(counter + 1, 'X')
            counter += 1
        else:
            counter += 2
    return plaintext

def process_arguments():
    parser = argparse.ArgumentParser(description='Encode and decode Playfair cipher.', epilog='Developer: Migdalo')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--encode', action='store_true', help='Encode Playfair cipher.')
    group.add_argument('-d', '--decode', action='store_true', help='Decode Playfair cipher.')
    parser.add_argument('-k', '--key', help='Key. If none is given a default key ("playfair example") is used.')
    parser.add_argument('-a', help='Try to get the key with known plaintext attack.')
    parser.add_argument('input', help='String you want to encode/decode.')
    args = parser.parse_args()
    
    if args.encode:
        print(encode_playfair(args.input, args.key))
    elif args.decode:
        print(decode_playfair(args.input, args.key))

''' Main '''
if __name__ == '__main__':
    process_arguments()
    
