import os

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import zlib
import base64


# Our Encryption Function
def rsa_encrypt(blob, public_key, extension):
    # Import the Public Key and use for encryption using PKCS1_OAEP
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    # compress the data first
    blob = zlib.compress(blob)

    # In determining the chunk size, determine the private key length used in bytes
    # and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
    # in chunks
    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted = b""

    while not end_loop:
        # The chunk
        chunk = blob[offset:offset + chunk_size]

        # If the data chunk is less then the chunk size, then we need to add
        # padding with " ". This indicates the we reached the end of the file
        # so we end loop here
        if len(chunk) % chunk_size != 0:
            end_loop = True
            chunk += b" " * (chunk_size - len(chunk))

        # Append the encrypted chunk to the overall encrypted file
        encrypted += rsa_key.encrypt(chunk)

        # Increase the offset by chunk size
        offset += chunk_size

    # Base 64 encode the encrypted file
    encrypted += b"\x00\x00\x00\x00"
    ext = rsa_key.encrypt(b"extension=" + extension.encode('utf-8'))
    encrypted += ext
    return base64.b64encode(encrypted)


def rsa_decrypt(encrypted_blob, private_key, passphrase):
    # Import the Private Key and use for decryption using PKCS1_OAEP
    rsakey = RSA.importKey(private_key, passphrase)
    rsakey = PKCS1_OAEP.new(rsakey)

    # Base 64 decode the data
    encrypted_blob = base64.b64decode(encrypted_blob)
    index = encrypted_blob.find(b"\x00\x00\x00\x00")
    ext = encrypted_blob[index + 4:]
    file_extension = rsakey.decrypt(ext)[-3:].decode("utf-8")
    encrypted_blob = encrypted_blob[0:index]

    # In determining the chunk size, determine the private key length used in bytes.
    # The data will be in decrypted in chunks
    chunk_size = 512
    offset = 0
    decrypted = b""

    # keep loop going as long as we have chunks to decrypt
    while offset < len(encrypted_blob):
        # The chunk
        chunk = encrypted_blob[offset: offset + chunk_size]

        # Append the decrypted chunk to the overall decrypted file
        decrypted += rsakey.decrypt(chunk)

        # Increase the offset by chunk size
        offset += chunk_size

    # return the decompressed decrypted data
    return zlib.decompress(decrypted), file_extension


def get_rsa_keys():
    if not os.path.exists('keys/private_key.pem'):
        create_rsa_key('12345')
    priv_key = open("keys/private_key.pem", "rb")
    private_key = priv_key.read()
    priv_key.close()
    pub_key = open("keys/public_key.pem", "rb")
    public_key = pub_key.read()
    pub_key.close()
    return public_key, private_key


def create_rsa_key(passphrase):
    # Generate a public/ private key pair using 4096 bits key length (512 bytes)
    new_key = RSA.generate(4096, e=65537)
    # The private key in PEM format
    private_key = new_key.exportKey("PEM", passphrase)

    # The public key in PEM Format
    public_key = new_key.publickey().exportKey("PEM")

    fd = open("keys/private_key.pem", "wb")
    fd.write(private_key)
    fd.close()

    fd = open("keys/public_key.pem", "wb")
    fd.write(public_key)
    fd.close()

