from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import os

def decrypt_private_key(usb_path, pin, progress_callback):
    try:
        enc_file = None
        for root, dirs, files in os.walk(os.path.join(usb_path, "keys")):
            for f in files:
                if f.endswith("_private_key.enc"):
                    enc_file = os.path.join(root, f)
                    break
        if enc_file is None:
            return None

        with open(enc_file, "rb") as f:
            data = f.read()

        salt = data[:16]
        nonce = data[16:32]
        tag = data[32:48]
        ciphertext = data[48:]

        key = None
        iterations = 600000
        
        # use PBKDF2 to get the key from the pin and salt
        for i in range(iterations):
            key = PBKDF2(pin, salt, dkLen=32, count=1) if key is None else PBKDF2(pin, salt, dkLen=32, count=1, prf=lambda p, s: key)
            if i % 1000 == 0:
                progress_callback(i + 1, iterations)

        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        private_key = cipher.decrypt_and_verify(ciphertext, tag)
        return private_key

    except Exception as e:
        print(f"[decrypt_private_key] Error: {e}")
        return None
