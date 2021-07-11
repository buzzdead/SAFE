import RSA
import ScreenShot


def take_screenshot():
    ScreenShot.activateScreenShot()
    pubkey, privkey = RSA.get_rsa_keys()
    ctxt = RSA.rsa_encrypt2("files/saved.png", pubkey)
    fd = open("files/encrypted", "wb")
    fd.write(ctxt)
    fd.close()


def decrypt_file():
    pubkey, privkey = RSA.get_rsa_keys()
    fd = open("files/encrypted", "rb")
    ctxt = fd.read()
    fd.close()
    RSA.rsa_decrypt2(ctxt, privkey)


def generate_keys():
    RSA.create_rsa_key('12345')
