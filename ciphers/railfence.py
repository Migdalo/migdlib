""" Rail Fence cipher """
import argparse
import string

""" Get rail separator character """
def get_separator(cipher):
    if '.' in cipher:
        for i in string.punctuation:
            if i not in cipher:
                return i
    else:
        return '.'
    
""" Get an array representation of the rails used in encryption/decryption. """
def get_rails(raillen, railcount, cipher, separator='.'):
    goingup = False
    rails = []
    count = 0
    nextrail = 0
    
    # Create rails
    for i in range(railcount):
        rails.append([])
        
    # Add cipher to rail
    for i in range(raillen):
        for rail in range(len(rails)):
            try:
                c = cipher[count]
            except:
                continue
            if nextrail == rail:
                rails[rail].append(c)
                count += 1
                if nextrail == railcount - 1:
                    goingup = True
                elif nextrail == 0:
                    goingup = False
            else:
                rails[rail].append(separator)
            
        if goingup:
            nextrail -= 1
        else:
            nextrail += 1
    
    return rails
    
""" Brute-force the correct rail. """
def brute_fence_rail(cipher, keyword='', printrails=False):
    # Go through all possible rails
    for rail in range(3, len(cipher)):
        s = decrypt_rail_fence(cipher, rail, printrails)
        if not keyword or keyword in s:
            print(s)

""" Decrypt rail-fence cipher """
def decrypt_rail_fence(cipher, railcount=3, printrails=False):
    raillen = len(cipher)
    cipher = cipher.replace(' ', '')
    separator = get_separator(cipher)
    rails = []
    placeholder = '*'
    count = 0
    
    # Get empty rails
    emptyrails = get_rails(raillen, railcount, placeholder * raillen, separator)
    
    # Add cipher to empty rails
    for rail in range(railcount):
        rails.append([])
        for i in range(raillen):
            try:
                c = emptyrails[rail][i]
            except:
                rails[rail].append(separator)
                continue
            if c == placeholder:
                rails[rail].append(cipher[count])
                count += 1
            else:
                rails[rail].append(emptyrails[rail][i])
    
    if printrails:
        for rail in rails:
            print(''.join(rail))
        
    # Print only the result without the rails
    solution = ''
    for column in range(raillen):
        for rail in rails:
            if rail[column] is not separator:
                solution += rail[column]
    return solution
    
""" Encrypt Rail Fence cipher """
def encrypt(cipher, railcount=3, printrails=False):
    separator = get_separator(cipher)
    cipher = cipher.replace(' ', '')
    rails = get_rails(len(cipher), railcount, cipher, separator)
    output = ''
    for rail in rails:
        if printrails:
            print(''.join(rail))
        output += ''.join(rail).replace(separator, '')
    return output

""" Process command-line arguments """
def process_arguments():
    parser = argparse.ArgumentParser(description='Encrypt and decrypt Rail Fence cipher.', conflict_handler='resolve')
    parser.add_argument('text', help='Text you want to encrypt/decrypt.')
    parser.add_argument('-r', '--rail', type=int, default=3, help='Number of rails to use (default: 3).')
    encgroup = parser.add_argument_group('Encryption')
    encgroup.add_argument('-e', '--encrypt', action='store_true', help='Encrypt Rail Fence cipher.')
    decgroup = parser.add_argument_group('Decryption')
    decgroup.add_argument('-d', '--decrypt', action='store_true', help='Decrypt Rail Fence cipher.')
    decgroup.add_argument('-b', '--brute', action='store_true', help='Brute-force the correct railnumber.')
    decgroup.add_argument('-k', '--keyword', help='Keyword you expect to find. Used with -b.')
    parser.add_argument('-p', '--printrails', action='store_true', help='Print the rails.')
    args = parser.parse_args()
    
    if args.encrypt and args.decrypt:
        print('Can\'t use both -e and -d at the same time.')
        return 1
    if args.encrypt:
        print(encrypt(args.text, args.rail, args.printrails))
    elif args.decrypt:
        if args.brute:
            brute_fence_rail(args.text, args.keyword, args.printrails)
        else:
            print(decrypt_rail_fence(args.text, args.rail, args.printrails))

""" Main """
if __name__ == '__main__':
    process_arguments()
    
