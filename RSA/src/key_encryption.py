from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import os

def encrypt_private_key(private_key, pin, progress_callback):
    """! 
    @brief Encrypts a private key using AES symetric encryption, where the encryption key is the user-provided PIN using PBKDF2 (Password-Based Key Derivation Function 2).

    @details
    The resulting encrypted output is composed of: 
        salt (16 bytes) + nonce (16 bytes) + authentication tag (16 bytes) + ciphertext (N bytes).

    @param private_key (bytes)  The private key to encrypt.
    @param pin (str)  The password used to derive the encryption key.
    @param progress_callback (Callable[[int, int], None])  A callback function to update the GUI progress bar.

    @return  The encrypted private key as bytes, or None if an error occurs.
    """
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