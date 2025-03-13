from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import os

def encrypt_private_key(private_key, pin, progress_callback):
    try:
        salt = os.urandom(16)  # 128-bit salt (16 bytes)
        iterations = 600000
        key = None
        
        for i in range(iterations):
            key = PBKDF2(pin, salt, dkLen=32, count=1) if key is None else \
                  PBKDF2(pin, salt, dkLen=32, count=1, prf=lambda p, s: key)
            if i % 1000 == 0: 
                progress_callback(i + 1, iterations) # update GUI progress bar every 1000 iterations
        
        cipher = AES.new(key, AES.MODE_EAX)
        encrypted_key, tag = cipher.encrypt_and_digest(private_key)
        return salt + cipher.nonce + tag + encrypted_key
    except Exception as e:
        print(f"Error encrypting private key: {e}")
        return None