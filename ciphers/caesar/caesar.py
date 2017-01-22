""" Encrypt and decrypt Caesar cipher. """
from __future__ import print_function
import string
import argparse

def discover_alphabet(convertable, nonumbers=False):
    """ Get an alphabet range to use. """
    alphabet = []
    has_upper = False
    has_lower = False
    has_digits = False
    for char in convertable:
        if char not in alphabet:
            if char in string.ascii_lowercase:
                has_lower = True
            elif char in string.ascii_uppercase:
                has_upper = True
            elif not nonumbers and char in string.digits:
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

def rotate_char(char, rotation, alphabet):
    """ Rotates a single character. """
    tmp = alphabet.index(char) + rotation
    while tmp >= len(alphabet):
        tmp = tmp - len(alphabet)
    return alphabet[tmp]

def rotate(convertable, rot=13, alphabet='', nonumbers=False, sametype=False):
    """ Rotate characters """
    plain = []

    if not sametype:
        if not alphabet:
            alphabet = discover_alphabet(convertable, nonumbers)

        # If rotation is larger than the alphabet length
        while rot > len(alphabet):
            rot = rot - len(alphabet)

    # Rotate all characters in the input string
    for char in convertable:
        if nonumbers and char in string.digits:
            plain.append(char)
        elif sametype:
            if char in string.ascii_uppercase:
                plain.append(rotate_char(char, rot, string.ascii_uppercase))
            elif char in string.ascii_lowercase:
                plain.append(rotate_char(char, rot, string.ascii_lowercase))
            elif char in string.digits:
                plain.append(rotate_char(char, rot, string.digits))
            else:
                plain.append(char)
        elif char not in alphabet:
            plain.append(char)
        else:
            plain.append(rotate_char(char, rot, alphabet))
    return ''.join(plain)

def solve_rotation(convertable, keyword, nonumbers=False, sametype=False):
    """ Brute-force all possible rotations """
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
    """ Process user arguments. """
    parser = argparse.ArgumentParser(description=\
        'Encode and decode Caesar cipher.', \
        epilog='Author: Migdalo (https://github.com/Migdalo)')
    parser.add_argument('text', help='The text you want to rotate.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--rotation', type=int, help=\
        'Number of rotations you want to do. ' +\
        'Use negative numbers to decipher. Default is 13.')
    group.add_argument('-b', '--brute', action='store_true', \
        help='Print all rotation options.')
    parser.add_argument('-k', '--keyword', \
        help='Keyword you want to find. Usable with -b.')
    parser.add_argument('-n', '--nonumbers', action='store_true', \
        help='Don\'t rotate numbers.')
    parser.add_argument('-s', '--sametype', action='store_true', help=\
        'Don\'t allow character type to change. E.g. uppercase ' +\
        'character can only be replaces by another uppercase character.')
    args = parser.parse_args()

    if args.brute:
        solve_rotation(args.text, args.keyword, args.nonumbers, args.sametype)
    elif args.rotation:
        print(rotate(args.text, args.rotation, nonumbers=args.nonumbers, \
            sametype=args.sametype))
    else:
        print(rotate(args.text, nonumbers=args.nonumbers, sametype=args.sametype))

if __name__ == '__main__':
    process_args()
