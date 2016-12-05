import string
import argparse

""" Caesar cipher """

""" Get an alphabet range to use. """
def discover_alphabet(convertable, nonumbers):
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

""" Rotate characters """
def rotate(convertable, rot=13, alphabet='', nonumbers=False):
    plain = []
    
    if not alphabet:
        alphabet = discover_alphabet(convertable, nonumbers)
    
    # If rotation is larger than the alphabet length
    if rot > len(alphabet):
        rot = rot - len(alphabet)
    
    # Rotate all characters in the input string
    try:
        for c in convertable:
            if nonumbers and c in string.digits:
                plain.append(c)
            elif c not in alphabet:
                plain.append(c)
            else:
                tmp = alphabet.index(c) + rot
                if tmp >= len(alphabet):
                    tmp = tmp - len(alphabet)
                plain.append(alphabet[tmp])
        return ''.join(plain)
    except:
        return ''

""" Brute-force all possible rotations """
def solve_rotation(convertable, keyword, nonumbers):
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
    parser = argparse.ArgumentParser(description='Encode and decode Caesar cipher.', epilog='Developer: Migdalo')
    parser.add_argument('text', help='The text you want to rotate.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--rotation', type=int, help='Number of rotations you want to do. ' +
            'Use negative numbers to decipher. Default is 13.')
    group.add_argument('-b', '--brute', action='store_true', help='Print all rotation options.')
    parser.add_argument('-k',  '--keyword', help='Keyword you want to find. Usable with -b.')
    parser.add_argument('-n', '--nonumbers', action='store_true', help='Don\'t rotate numbers.')
    args = parser.parse_args()
    
    if args.brute:
        solve_rotation(args.text, args.keyword, args.nonumbers)
    elif args.rotation:
        print(rotate(args.text, args.rotation, nonumbers=args.nonumbers))
    else:
        print(rotate(args.text, nonumbers=args.nonumbers))

if __name__ == '__main__':
    process_args()
