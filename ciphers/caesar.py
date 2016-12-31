import string
import argparse

""" Caesar cipher """

""" Get an alphabet range to use. """
def discover_alphabet(convertable, nonumbers=False, addpunct=False):
    alphabet = []
    has_upper = False
    has_lower = False
    has_digits = False
    for c in convertable:
        if c not in alphabet:
            if c in string.ascii_lowercase:
                has_lower = True
            elif c in string.ascii_uppercase:
                has_upper = True
            elif not nonumbers and c in string.digits:
                has_digits = True
        if has_digits and has_lower and has_upper:
            break
        elif nonumbers and has_lower and has_upper:
            break
            
    if has_lower:
        alphabet.append(string.ascii_lowercase)
    if has_upper:
        alphabet.append(string.ascii_uppercase)
    if has_digits:
        alphabet.append(string.digits)
    return ''.join(alphabet)

""" Rotates a single character. """
def rotate_char(char, rotation, alphabet):
    tmp = alphabet.index(char) + rotation
    while tmp >= len(alphabet):
        tmp = tmp - len(alphabet)
    return alphabet[tmp]

""" Rotate characters """
def rotate(convertable, rot=13, alphabet='', nonumbers=False, sametype=False):
    plain = []
    
    if not sametype:
        if not alphabet:
            alphabet = discover_alphabet(convertable, nonumbers)
        
        # If rotation is larger than the alphabet length
        while rot > len(alphabet):
            rot = rot - len(alphabet)
    
    # Rotate all characters in the input string
    for c in convertable:
        if nonumbers and c in string.digits:
            plain.append(c)
        elif sametype:
            if c in string.ascii_uppercase:
                plain.append(rotate_char(c, rot, string.ascii_uppercase))
            elif c in string.ascii_lowercase:
                plain.append(rotate_char(c, rot, string.ascii_lowercase))
            elif c in string.digits:
                plain.append(rotate_char(c, rot, string.digits))
            else:
                plain.append(c)
        elif c not in alphabet:
            plain.append(c)
        else:
            plain.append(rotate_char(c, rot, alphabet))
    return ''.join(plain)

""" Brute-force all possible rotations """
def solve_rotation(convertable, keyword, nonumbers=False, sametype=False):
    if not sametype:
        alphabet = discover_alphabet(convertable, nonumbers)
    print('{0: <5}'.format('ROT'), convertable)
    print('-' * 20)
    
    # Print all possible rotations
    for i in range(len(alphabet)):
        if not keyword:
            print('{0: <5}'.format(str(i)), rotate(convertable, i, alphabet, nonumbers))
        else:
            solution = rotate(convertable, i, alphabet, nonumbers)
            if keyword in solution:
                print('{0: <5}'.format(str(i)), solution)
                return

def process_args():
    parser = argparse.ArgumentParser(description='Encode and decode Caesar cipher.', epilog='Author: Migdalo')
    parser.add_argument('text', help='The text you want to rotate.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--rotation', type=int, help='Number of rotations you want to do. ' +
            'Use negative numbers to decipher. Default is 13.')
    group.add_argument('-b', '--brute', action='store_true', help='Print all rotation options.')
    parser.add_argument('-k', '--keyword', help='Keyword you want to find. Usable with -b.')
    parser.add_argument('-n', '--nonumbers', action='store_true', help='Don\'t rotate numbers.')
    parser.add_argument('-s', '--sametype', action='store_true', help='Don\'t allow character type to change.' +
            ' Force uppercase characters to rotate to another uppercase character and so forth.')
    args = parser.parse_args()
    
    if args.brute:
        solve_rotation(args.text, args.keyword, args.nonumbers, args.sametype)
    elif args.rotation:
        print(rotate(args.text, args.rotation, nonumbers=args.nonumbers, sametype=args.sametype))
    else:
        print(rotate(args.text, nonumbers=args.nonumbers, sametype=args.sametype))

if __name__ == '__main__':
    process_args()
    
