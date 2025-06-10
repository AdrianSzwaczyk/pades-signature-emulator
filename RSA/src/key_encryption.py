"""!
@file key_encryption.py
@brief Contains the function to encrypt a private key using AES symmetric encryption with a PIN given by the user.
"""

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import os

def encrypt_private_key(private_key, pin, progress_callback):
    """! 
    @brief Encrypts a private key using AES symetric encryption, where the encryption key is the user-provided PIN using PBKDF2 (Password-Based Key Derivation Function 2).

    @details
    Derives a 256-bit AES key from a user-provided PIN using PBKDF2 with a 128-bit random salt and 600,000 iterations. The private key is encrypted using AES in EAX mode.

    Used libraries:
    - `pycryptodome` – for AES and PBKDF2 (`Crypto.Cipher.AES`, `Crypto.Protocol.KDF`)
    - `os` – for secure salt generation

    @param private_key (bytes)  The private key to encrypt.
    @param pin (str)  The password used to derive the encryption key.
    @param progress_callback (Callable[[str], None])  A callback function to update the GUI progress with a status message.

    @return  The encrypted private key as bytes, or None if an error occurs.
    The resulting encrypted output is composed of: 
        salt (16 bytes) + nonce (16 bytes) + authentication tag (16 bytes) + ciphertext (N bytes).
    """
    try:
        salt = os.urandom(16)  # 128-bit salt (16 bytes)
        iterations = 600000
        key = PBKDF2(pin, salt, dkLen=32, count=iterations)
        progress_callback("Encrypting...")
        cipher = AES.new(key, AES.MODE_EAX)
        encrypted_key, tag = cipher.encrypt_and_digest(private_key)
        return salt + cipher.nonce + tag + encrypted_key
    except Exception as e:
        print(f"Error encrypting private key: {e}")
        return None