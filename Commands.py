import ntpath
import os

import RSA
import ScreenShot


def encrypt_file(in_file, out_file, remove_file):
    pubkey, privkey = RSA.get_rsa_keys()
    plaintext_file = open(in_file, 'rb')
    plaintext = plaintext_file.read()
    plaintext_file.close()

    ext = path_leaf(in_file)[1]
    ciphertext = RSA.rsa_encrypt(plaintext, pubkey, ext)
    print(ciphertext)
    ciphertext_file = open(out_file, 'wb')
    ciphertext_file.write(ciphertext)
    ciphertext_file.close()

    if remove_file:
        os.remove(in_file)


def take_screenshot():
    ScreenShot.activateScreenShot()


def decrypt_file(in_file, out_file):
    pubkey, privkey = RSA.get_rsa_keys()
    fd = open("encrypted_files/" + in_file, "rb")
    ctxt = fd.read()
    fd.close()

    plaintext, extension = RSA.rsa_decrypt(ctxt, privkey, '12345')
    if out_file:
        filename = path_leaf(in_file)[3]
        plaintext_file = open('files/' + filename + '.' + extension, 'wb')
        plaintext_file.write(plaintext)
        plaintext_file.close()
    else:
        return plaintext


def generate_keys():
    RSA.create_rsa_key('12345')


def path_leaf(path):
    head, tail = ntpath.split(path)
    filename, file_extension = os.path.splitext(path)
    return tail or ntpath.basename(head), file_extension, head, filename
