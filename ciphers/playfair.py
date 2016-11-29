'''
Playfair cipher

'''
import argparse

playfair_matrix = [['P', 'L', 'A', 'Y', 'F'], 
          ['I', 'R', 'E', 'X', 'M'], 
          ['B', 'C', 'D', 'G', 'H'], 
          ['K', 'N', 'O', 'Q', 'S'], 
          ['T', 'U', 'V', 'W', 'Z']]

def get_new_pos(pos, shift_col, shift_row):
    global playfair_matrix
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

'''
Decryption

'''
def decode_block(char1, char2):
    global playfair_matrix
    pos1 = (0, 0)
    pos2 = (0, 0)
    
    # Find the char position in playfair matrix
    for line in range(len(playfair_matrix)):
        if char1 in playfair_matrix[line]:
            pos1 = (line, playfair_matrix[line].index(char1))
        if char2 in playfair_matrix[line]:
            pos2 = (line, playfair_matrix[line].index(char2))
          
    if pos1[0] == pos2[0]: # Both chars on same line
        return get_new_pos(pos1, 0, -1) + get_new_pos(pos2, 0, -1)
    elif pos1[1] == pos2[1]: # Both chars on same column
        return get_new_pos(pos1, -1, 0) + get_new_pos(pos2, -1, 0)
    else: # Square
        return playfair_matrix[pos1[0]][pos2[1]] + playfair_matrix[pos2[0]][pos1[1]]

def decode_playfair(cipherinput):
    results = ''
    
    # Make sure the input is a list with two chars as elements
    cipher = cipherinput.split()
    if len(cipher) == 1:
        cipher = []
        for i in range(0, len(cipherinput), 2):
            cipher.append(cipherinput[i:i+2])
            
    # Decode
    for tc in cipher:
        results += decode_block(tc[0], tc[1])
    
    return results

'''
Encryption

'''
def encode_block(char1, char2):
    global playfair_matrix
    pos1 = (0, 0)
    pos2 = (0, 0)
    
    # Find the char position in playfair matrix
    for line in range(len(playfair_matrix)):
        if char1 in playfair_matrix[line]:
            pos1 = (line, playfair_matrix[line].index(char1))
        if char2 in playfair_matrix[line]:
            pos2 = (line, playfair_matrix[line].index(char2))
    
    # Encode the position
    if pos1[0] == pos2[0]: # Both chars on same line
        return get_new_pos(pos1, 0, 1) + get_new_pos(pos2, 0, 1)
    elif pos1[1] == pos2[1]: # Both chars on same column
        return get_new_pos(pos1, 1, 0) + get_new_pos(pos2, 1, 0)
    else: # Square
        return playfair_matrix[pos1[0]][pos2[1]] + playfair_matrix[pos2[0]][pos1[1]]

def encode_playfair(plaintext):
    cipher = ''
    plaintext = list(''.join(plaintext.split()))
    plain = []
    counter = 0
    
    # Handle double characters
    while counter < len(plaintext) - 1:
        if plaintext[counter] == plaintext[counter + 1]:
            plaintext.insert(counter + 1, 'X')
            counter += 1
        else:
            counter += 2
    
    # Change the user input to be a list with two chars as elements
    for i in range(0, len(plaintext), 2):
        plain.append(plaintext[i:i+2])
    
    # Encode
    for tc in plain:
        cipher += encode_block(tc[0], tc[1])
    return cipher

'''
Main

'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encode and decode Playfair cipher.', epilog='Developer: Migdalo')
    parser.add_argument('-e', '--encode', help='Encode Playfair cipher.')
    parser.add_argument('-d', '--decode', help='Decode Playfair cipher.')
    args = parser.parse_args()
    
    if args.encode:
        print encode_playfair(args.encode)
    elif args.decode:
        print decode_playfair(args.decode)
