"""!
@file key_generation.py
@brief Contains the function to generate RSA keys in .PEM format.
"""

from Crypto.PublicKey import RSA

def generate_rsa_keys():
    """! 
    @brief Generating two RSA keys: a private key and a public key (4096 bits). Both keys are stored in PEM format in bytes format.

    @details
    This function uses the `Crypto.PublicKey.RSA` module from the `pycryptodome` package to generate a secure RSA key pair.
    The private and public keys are exported in .PEM format as bytes.

    @return Tuple ([str | None, str | None]): containing the private key and public key in bytes format. If an error occurs, returned tuple is (None, None).
    """
    try:
        key = RSA.generate(4096) # 4096-bit RSA key
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key
    except Exception as e:
        print(f"Error generating RSA keys: {e}")
        return None, None