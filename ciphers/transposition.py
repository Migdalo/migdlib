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

def print_table(table):
    end = 0
    for line in range(len(table)):
        for c in range(len(table[line])):
            if table[line][c] == '':
                end = c
                
        print(table[line][:len(table[line])-end])
         
""" Decrypt transposition cipher """
def decode_transposition(ciphertext, key, printtable=False):
    ciphertext = ciphertext.upper()
    key = key.upper()
    transposition_table = []
    count = 0
    r_table = []
    keylen = len(key)
    
    tableheight = int(len(ciphertext) / len(key))
    if len(ciphertext) % len(key) == 0:
        uneven = False
    else:
        uneven = True
    
    # Get value for each char in the key 
    values = sorted(count_key_values(key))
    
    # Add ciphertext to transposition table
    for j in range(keylen):
        transposition_table.append([])
        for i in range(tableheight):
            transposition_table[j].append(ciphertext[count])
            count += 1
        if uneven:
            if count > len(ciphertext) - len(key) + 1:
                transposition_table[j].append(ciphertext[count])
            else:
                transposition_table[j].append('')
                
        # Add the key to the table
        r_table.append((values[j][0], transposition_table[j]))
    
    # Sort list based on keyword
    e_table = []
    for j in range(keylen):
        for i in range(keylen):
            if key[j] == r_table[i][0]:
                e_table.append(r_table[i][1])
    
    # Join table to plaintext
    t_table = list(zip(*e_table))
    
    # Print encryption matrix
    if printtable:
        print_table(t_table)
      
    a = [''.join(t) for t in t_table]
    return ''.join(a)

""" Encrypt transposition cipher """
def encode_transposition(plaintext, key, printtable=False):
    plaintext = plaintext.upper()
    key = key.upper()
    values = count_key_values(key)
    transposition_table = []
    count = 0
    
    # Calculate height of the table
    if len(plaintext) % len(key) is not 0:
        tableheigth = int(len(plaintext) / len(key) + 1)
    else:
        tableheigth = len(plaintext) / len(key)
    
    # Add plaintext to transposition table
    for i in range(tableheigth):
        transposition_table.append([])
        for j in range(len(key)):
            try:
                transposition_table[i].append(plaintext[count])
                count += 1
            except IndexError:
                # Handle instances where plaintext length is 
                # not divisible by key length.
                transposition_table[i].append('')
    
    # Print encryption matrix
    if printtable:
        print_table(transposition_table)
    
    # Lines to columns and columns to lines
    t_table = list(zip(*transposition_table))
    r_table = []
    
    # Combine values[1] and t_table as a list of tuples
    for i in range(len(values)):
        try:
            r_table.append((values[i][1], t_table[i]))
        except IndexError:  
            continue
     
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
    parser.add_argument('-t', '--table', action='store_true', help='Print the encryption table.')
    args = parser.parse_args()
    
    if args.encode:
        print(encode_transposition(args.text, args.key, args.table))
    elif args.decode:
        print(decode_transposition(args.text, args.key, args.table))
