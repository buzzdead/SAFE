import os

from Crypto.PublicKey import RSA


def get_rsa_keys():
    if not os.path.exists('keys/private_key.pem'):
        create_rsa_key()
    priv_key = open("keys/private_key.pem", "rb")
    private_key = priv_key.read()
    priv_key.close()
    pub_key = open("keys/public_key.pem", "rb")
    public_key = pub_key.read()
    pub_key.close()
    return public_key, private_key


def create_rsa_key():
    # Generate a public/ private key pair using 4096 bits key length (512 bytes)
    new_key = RSA.generate(2048, e=65537)
    # The private key in PEM format
    private_key = new_key.exportKey("PEM")

    # The public key in PEM Format
    public_key = new_key.publickey().exportKey("PEM")

    fd = open("keys/private_key.pem", "wb")
    fd.write(private_key)
    fd.close()

    fd = open("keys/public_key.pem", "wb")
    fd.write(public_key)
    fd.close()
