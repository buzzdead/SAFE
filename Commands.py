import os

import RSA
import ScreenShot


def encrypt_file(fileName):
    pubkey, privkey = RSA.get_rsa_keys()
    ctxt = RSA.rsa_encrypt2("files/saved.png", pubkey)
    fd = open(fileName, "wb")
    fd.write(ctxt)
    fd.close()
    os.remove("files/saved.png")

def take_screenshot():
    ScreenShot.activateScreenShot()

def decrypt_file(fileName):
    pubkey, privkey = RSA.get_rsa_keys()
    fd = open("encrypted_files/" + fileName, "rb")
    ctxt = fd.read()
    fd.close()
    RSA.rsa_decrypt2(ctxt, privkey, fileName)


def generate_keys():
    RSA.create_rsa_key('12345')
