"""!
@file decrypt_key.py
@brief Contains the function to decrypt an RSA private key stored on a USB device.
"""

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import os

def decrypt_private_key(usb_path, pin, progress_callback):
    """!
    @brief Decrypts an RSA private key stored on a USB device using AES and a PIN-based key derivation.

    @details This function looks for an encrypted private key file inside the "keys" folder on the specified in params USB path.  
    It reads the encrypted data and derives the AES key from the user-provided PIN using PBKDF2 with a 128-bit salt and 600,000 iterations.  
    Decryption is done using AES in EAX mode. Progress updates are reported every 1000 iterations with the callback function.

    The function uses the following libraries:
    - 'pycryptodome' – Crypto.Protocol.KDF.PBKDF2, Crypto.Cipher.AES
    - 'os' – to search for the encrypted file on the USB drive

    @param usb_path (str): The path to the USB device where the encrypted private key is stored.
    @param pin (str): The PIN used to derive the decryption key.
    @param progress_callback Callable[[int, int], None]: A callback function to show decryption progress.

    @return bytes | None: The decrypted private key (in bytes) if successful, or None if an error occurs or the key file is missing.
    """
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
