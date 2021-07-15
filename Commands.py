import hashlib
import ntpath
import os

import AES
import RSA
import SAFE
import ScreenShot


def encrypt_file(in_file, out_file, remove_file):
    plaintext_file = open(in_file, 'rb')
    plaintext = plaintext_file.read()
    plaintext_file.close()

    ext = path_leaf(in_file)[1]
    ciphertext = AES.encrypt(plaintext, SAFE.rsa_key, ext)

    ciphertext_file = open(out_file, 'wb')
    ciphertext_file.write(ciphertext)
    ciphertext_file.close()

    if remove_file or in_file == 'files/saved.png':
        os.remove(in_file)


def take_screenshot():
    ScreenShot.activateScreenShot()


def decrypt_file(in_file, out_file):
    fd = open("encrypted_files/" + in_file, "rb")
    ctxt = fd.read()
    fd.close()

    plaintext, hsh = AES.decrypt(ctxt, SAFE.rsa_key)
    ext_length = plaintext[-1:]
    ext_length = bytes.decode(ext_length, 'utf-8')
    ext = bytes.decode(plaintext[-int(ext_length) - 1: - 1], 'utf-8')
    org_hash = hashlib.sha256(plaintext[0:len(plaintext) - int(ext_length) - 1]).digest()
    if hsh != org_hash:
        print("Returning now")
    else:
        print("Yohoo, integrity maintained")

    if out_file:
        filename = path_leaf(in_file)[3]
        plaintext_file = open('files/' + filename + ext, 'wb')
        plaintext_file.write(plaintext[0:len(plaintext) - int(ext_length) - 1])
        plaintext_file.close()
    else:
        return plaintext[0:len(plaintext) - int(ext_length) - 1]


def generate_keys():
    RSA.create_rsa_key()
    priv = open('keys/private_key.pem', 'rb')
    priv_text = priv.read()
    priv.close()
    enc_key = AES.encrypt(priv_text, SAFE.rsa_key, '.pem')
    priv = open('keys/private_key.pem', 'wb')
    priv.write(enc_key)
    priv.close()
    SAFE.rsa_key = activated(SAFE.rsa_key)[0]


def path_leaf(path):
    head, tail = ntpath.split(path)
    filename, file_extension = os.path.splitext(path)
    return tail or ntpath.basename(head), file_extension, head, filename


def activated(password):
    try:
        fd = open('keys/private_key.pem', 'rb')
        ctxt = fd.read()
        rsa_key, hsh = AES.decrypt(ctxt, password)
        hsh2 = hashlib.sha256(rsa_key).digest()
        valid_key = hsh2 == hsh
        if not valid_key:
            print("Woops, its the wrong key")
        else:
            print("Screen and file encryption activated")
    except FileNotFoundError:
        return False
    return rsa_key, valid_key
