""" Transposition cipher """
import string
import argparse

def count_key_values(key):
    alphabet = []
    values = []
    alphabet = list(string.ascii_uppercase)
    
    for char in key:
        try:
            c = alphabet.index(char)
        except:
            c = -1
            
        values.append((char, c + 1))
    
    return values

""" Decrypt transposition cipher """
def decode_transposition(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()
    values = count_key_values(key)
    transposition_table = []
    count = 0
    
    # Add ciphertext to transposition table
    for j in range(len(key)):
        transposition_table.append([])
        for i in range(len(ciphertext) / len(key)):
            transposition_table[j].append(ciphertext[count])
            count += 1
    
    # Order the arrya and add the key to it
    values = sorted(values)
    r_table = []
    for i in range(len(values)):
        r_table.append((values[i][0], transposition_table[i]))
    
    # Sort list based on keyword
    e_table = []
    for i in range(len(values)):
        for j in range(len(values)):
            if key[i] == r_table[j][0]:
                e_table.append(r_table[j][1])
    
    # Join table to plaintext
    t_table = zip(*e_table)
    a = [''.join(t) for t in t_table]
    return ''.join(a)

""" Encrypt transposition cipher """
def encode_transposition(plaintext, key):
    plaintext = plaintext.upper()
    key = key.upper()
    values = count_key_values(key)
    transposition_table = []
    count = 0
    
    # Add plaintext to transposition table
    for i in range(len(plaintext) / len(key)):
        transposition_table.append([])
        for j in range(len(key)):
            transposition_table[i].append(plaintext[count])
            count += 1
    
    # Lines to columns and columns to lines
    t_table = zip(*transposition_table)
    r_table = []
    
    # Combine values[1] and t_table as a list of tuples
    for i in range(len(values)):
        r_table.append((values[i][1], t_table[i]))
    
    # Sort the table based on the key values and join lines to strings
    r_table = sorted(r_table, key=lambda t: t[0])
    a = [''.join(t[1]) for t in r_table]
    return ''.join(a)
    
""" Main """
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Encode and decode transposition cipher.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e', '--encode', action='store_true', help='Encrypt with transposition cipher.')
    group.add_argument('-d', '--decode', action='store_true', help='Decrypt with transposition cipher.')
    parser.add_argument('key', help='Key to use to encrypt/decrypt.')
    parser.add_argument('text', help='Text you want to encrypt/decrypt.')
    args = parser.parse_args()
    
    if args.encode:
        print(encode_transposition(args.text, args.key))
    elif args.decode:
        print(decode_transposition(args.text, args.key))
    
