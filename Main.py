import ScreenShot
import RSA

if __name__ == '__main__':
    ScreenShot.activateScreenShot()
    pubkey, privkey = RSA.get_rsa_keys()
    ctxt = RSA.rsa_encrypt2("saved.png", pubkey)
    fd = open("encrypted", "wb")
    fd.write(ctxt)
    fd.close()

    fd = open("encrypted", "rb")
    ctxt2 = fd.read()
    fd.close()
    RSA.rsa_decrypt2(ctxt2, privkey)

