def generate_rsa_keys():
    from Crypto.PublicKey import RSA
    try:
        key = RSA.generate(4096) # 4096-bit RSA key
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key
    except Exception as e:
        print(f"Error generating RSA keys: {e}")
        return None, None