import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Hash import MD5

class AES256:
    def __init__(self, key):
        self.bs = AES.block_size
        key = key.encode('utf-8')
        self.key = SHA256.new(key)
        self.iv = MD5.new(key)

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AES256.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def pad(m): # PKCS7
        return m+chr(16-len(m)%16)*(16-len(m)%16)
    
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
    
    def unpad(self, ct): # PKCS7
        return ct[:-ord(ct[-1])]
    
    def encrypt(self, raw):
        cipher = AES.new(self.key.digest(), AES.MODE_CBC, self.iv.digest())
        return cipher.encrypt(AES256.pad(raw).encode('utf-8')).hex()
"""
    def decrypt(self, enc):
        cipher = AES.new(self.key.digest(), AES.MODE_CBC, self.iv.digest())
        return AES256.unpad(cipher.decrypt(enc).hex())
"""