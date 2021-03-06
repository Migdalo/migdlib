import unittest
import subprocess
import caesar_cipher
import railfence
import os, sys
import playfair
import transposition
import vigenere

if os.name == 'posix' and sys.version_info[0] < 3:
    try:
        import subprocess32 as subprocess
    except:
        import subprocess
else:
    import subprocess

""" Test Caesar cipher """
class TestCaesarCipher(unittest.TestCase):
    def test_rotation(self):
        self.assertEqual(caesar_cipher.rotate('r0t4t10n_t3st', 13), '4d6h6ed0_6g56')
        
    def test_reverse_rotation(self):
        self.assertEqual(caesar_cipher.rotate('4d6h6ed0_6g56', -13), 'r0t4t10n_t3st')
        
    @unittest.expectedFailure
    def test_rotation_fail(self):
        self.assertEqual(caesar_cipher.rotate('r0t4t10n_t3st', 13, nonumbers=True), '4d6h6ed0_6g56')
    
""" Test Rail Fence cipher """
class TestRailFenceCipher(unittest.TestCase):

    def test_cli_commands(self):
        p = subprocess.check_output(['python', 'railfence.py', '-e', '-d', 'fleeatonce'])
        self.assertEqual(p, 'Can\'t use both -e and -d at the same time.\n')
    
    def test_encryption_simple(self):
        self.assertEqual(railfence.encrypt_rail_fence( \
        'WE ARE DISCOVERED. FLEE AT ONCE', 3), 'WECRFACERDSOEE.LETNEAIVDEO')
    
    def test_decryption_simple(self):
        self.assertEqual(railfence.decrypt_rail_fence( \
        'WECRFACERDSOEE.LETNEAIVDEO', 3), 'WEAREDISCOVERED.FLEEATONCE')
    
    def test_encryption_long(self):
        self.assertEqual(railfence.encrypt_rail_fence('A-fence-is-a-structure-that-encloses-an-area,-SharifCTF{QmFzZTY0IGlzIGEgZ2VuZXJpYyB0ZXJt},-typically-outdoors.', 21), 'AaY--rpyfneJBeaaX0n-,ZZcs-uXeeSVJ-sh2tioaZ}slrg,-ciE-anfGt.-eCIyss-TzprttFliora{GcouhQIadctm0ltt-FYluuezTyorZ-')
    
    def test_decryption_long(self):
        self.assertEqual(railfence.decrypt_rail_fence('AaY--rpyfneJBeaaX0n-,ZZcs-uXeeSVJ-sh2tioaZ}slrg,-ciE-anfGt.-eCIyss-TzprttFliora{GcouhQIadctm0ltt-FYluuezTyorZ-', 21), 'A-fence-is-a-structure-that-encloses-an-area,-SharifCTF{QmFzZTY0IGlzIGEgZ2VuZXJpYyB0ZXJt},-typically-outdoors.')
    
""" Test Playfair cipher """
class TestPlayfair(unittest.TestCase):
    def test_encryption(self):
        self.assertEqual(playfair.encode_playfair('Hide the gold in the tree stump', \
         'playfairexample'), 'BMNDWCXDKYBEKUDMLCXEIUUTIF')
    
    def test_decryption(self):
        self.assertEqual(playfair.decode_playfair('BMNDWCXDKYBEKUDMLCXEIUUTIF', \
        'playfairexample'), 'HIDETHEGOLDINTHETREXESTUMP')

""" Test Transposition cipher """
class TestTranspositionCipher(unittest.TestCase):
    def test_encode_equal_lenght(self):
        self.assertEqual(transposition.encode_transposition('theskyisblue', 'cat'), 'HKSUTSILEYBE')
        
    def test_decode_equal_lenght(self):
        self.assertEqual(transposition.decode_transposition('HKSUTSILEYBE', 'cat'), 'THESKYISBLUE')
        
    def test_encode_unequal_lenght(self):
        self.assertEqual(transposition.encode_transposition('theskyisbluesa', 'cat'), 'HKSUATSILSEYBE')
        
    def test_decode_unequal_lenght(self):
        self.assertEqual(transposition.decode_transposition('HKSUATSILSEYBE', 'cat'), 'THESKYISBLUESA')

""" Test Vigenere cipher """
class TestVigenereCipher(unittest.TestCase):
    @unittest.expectedFailure
    def test_cli_commands(self):
        p = subprocess.check_output(['python', 'vigenere.py', '-e', '-d'])
        self.expectedFailure(p)
        
    def test_encryption_basic(self):
        self.assertEqual(vigenere.encrypt_vigenere('ATTACKATDAWN', 'LEMON'), 'LXFOPVEFRNHR')
    
    def test_decryption_basic(self):
        self.assertEqual(vigenere.decrypt_vigenere('LXFOPVEFRNHR', 'LEMON'), 'ATTACKATDAWN')
        
    def test_encryption_basic(self):
        self.assertEqual(vigenere.encrypt_vigenere('attackatdawn', 'lemon'), 'LXFOPVEFRNHR')
    
    def test_decryption_basic(self): 
        self.assertEqual(vigenere.decrypt_vigenere('lxfopvefrnhr', 'lemon'), 'ATTACKATDAWN')
        
    def test_encryption_complex(self):
        self.assertEqual(vigenere.encrypt_vigenere('TEST{Let\'s_73st_s0meth1ng}', 'Pr0bl3m', \
        '[a-zA-Z0-9{}]'), 'wVGUjCq8\'J_V4Dk_EDD4usSzVq')
    
    def test_decryption_complex(self):
        self.assertEqual(vigenere.decrypt_vigenere('wVGUjCq8\'J_V4Dk_EDD4usSzVq', 'Pr0bl3m', \
        '[a-zA-Z0-9{}]'),'TEST{Let\'s_73st_s0meth1ng}')
        
    def test_encryption_complex_fail(self):
        with self.assertRaises(SystemExit):
            vigenere.encrypt_vigenere('TEST{Let\'s_73st_s0meth1ng}', 'Pr0bl3m', '[a-zA-Z{}]')
    
    def test_decryption_complex_fail(self):
        with self.assertRaises(SystemExit):
            vigenere.decrypt_vigenere('wVGUjCq8\'J_V4Dk_EDD4usSzVq', 'Pr0bl3m', '[a-zA-Z{}]')
    
if __name__ == '__main__':
    unittest.main()
