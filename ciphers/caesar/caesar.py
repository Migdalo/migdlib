""" Encrypt and decrypt Caesar cipher. """
from __future__ import print_function
import string
import argparse


class Caesar(object):

    def __init__(
            self, cipher_text, brute=False, rotations=13,
            keyword=None, nonumbers=False, sametype=True,
            alphabet=None):
        self.cipher_text = cipher_text
        self.brute = brute
        self.rot = rotations
        self.keyword = keyword
        self.nonumbers = nonumbers
        self.sametype = sametype
        self.alphabet = alphabet

    @staticmethod
    def rotate_char(char, rot, alphabet):
        """ Rotates a single character. """
        tmp = alphabet.index(char) + rot
        while tmp >= len(alphabet):
            tmp = tmp - len(alphabet)
        return alphabet[tmp]

    def solve(self):
        if self.brute:
            self.solve_rotation()
        else:
            print(self.rotate(self.rot))

    def solve_rotation(self):
        """ Brute-force all possible rotations """
        #if not self.sametype:
        self.alphabet = self.discover_alphabet(self.cipher_text, self.nonumbers)
        print('{0: <5}'.format('ROT'), self.cipher_text)
        print('-' * 20)

        # Print all possible rotations
        for i in range(len(self.alphabet)):
            if not self.keyword:
                print('{0: <5}'.format(str(i)), self.rotate(i))
            else:
                solution = self.rotate(i)
                if self.keyword in solution:
                    print('{0: <5}'.format(str(i)), solution)
                    return

    def rotate(self, rot):
        """ Rotate characters """
        plain = []

        if not self.sametype:
            if not self.alphabet:
                self.alphabet = self.discover_alphabet(self.cipher_text, self.nonumbers)

            # If rotation is larger than the alphabet length
            while rot > len(self.alphabet):
                rot = rot - len(self.alphabet)

        # Rotate all characters in the input string
        for char in self.cipher_text:
            if self.nonumbers and char in string.digits:
                plain.append(char)
            elif self.sametype:
                if char in string.ascii_uppercase:
                    plain.append(Caesar.rotate_char(char, rot, string.ascii_uppercase))
                elif char in string.ascii_lowercase:
                    plain.append(Caesar.rotate_char(char, rot, string.ascii_lowercase))
                elif char in string.digits:
                    plain.append(Caesar.rotate_char(char, rot, string.digits))
                else:
                    plain.append(char)
            elif char not in self.alphabet:
                plain.append(char)
            else:
                plain.append(Caesar.rotate_char(char, rot, self.alphabet))
        return ''.join(plain)

    def discover_alphabet(self, convertable, nonumbers=False):
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


def process_args():
    """ Process user arguments. """
    parser = argparse.ArgumentParser(description=\
        'Encode and decode Caesar cipher.', \
        epilog='Author: Migdalo (https://github.com/Migdalo)')
    parser.add_argument('text', help='The text you want to rotate.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--rotation', type=int, default=13, help=\
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

    cipher = Caesar(
        args.text, args.brute, args.rotation, args.keyword,
        args.nonumbers, args.sametype)
    cipher.solve()


if __name__ == '__main__':
    process_args()
