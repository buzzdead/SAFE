# AES 256 encryption/decryption using pycrypto library

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
pad = lambda s: s + bytes((BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(raw, password, ext):
    private_key = hashlib.sha256(password).digest()
    hsh = hashlib.sha256(raw).digest()

    if ext != '.pem':
        raw += bytes(ext + str(len(ext)), 'utf-8')

    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    raw = iv + cipher.encrypt(raw)
    raw += b'hashcode' + hsh
    return base64.b64encode(raw)


def decrypt(enc, password):
    private_key = hashlib.sha256(password).digest()
    enc = base64.b64decode(enc)
    pos = enc.find(b'hashcode')
    hsh = enc[pos + len(b'hashcode'):]
    enc = enc[0:pos]

    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    raw = unpad(cipher.decrypt(enc[16:]))
    return raw, hsh
