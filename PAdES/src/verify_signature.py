"""!
@file verify_signature.py
@brief Contains the function to verify the signature of a PDF file using a public RSA key.
"""

from pypdf import PdfReader
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def verify_pdf_signature(pdf_path, public_key_path):
    """! 
    @brief Verify the signature of a PDF file using a public key.

    @details This function opens and reads the PDF file with use of pypdf library, extracts metadata and checks if signature exists. If there is no data
    it returns False and proper error message. If the signature exists, it constructs PDF content as a text to compute the SHA256 digest and compares it with the stored digest.
    If those digests match, it means that the PDF has not been changed after signing with the private key. 
    Lastly, it reads the signature as bytes from earlier retrieved metadata, imports public key from the given path, and verifies the signature using the SHA256 digest
    and the public key.
    The function uses the following libraries: 
    - 'pypdf' for PDF parsing
    - Crypto.PublicKey.RSA, Crypto.Signature.pkcs1_15, Crypto.Hash.SHA256 from the 'pycryptodome' package for cryptographic operations.

    @param pdf_path (str)  The path to the PDF file to verify.
    @param public_key_path (str)  The path to the public key file in .PEM format.

    @return  tuple[bool, str] Where the first element is a boolean indicating whether the signature is valid or invalid. Second part is a string 
    with a message specifying the result of the verification process.
    """
    try:
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        if not metadata:
            return False, "No metadata found in the PDF file"
        if "/Signature" not in metadata or "/Digest" not in metadata:
            return False, "No signature found"

        signature_hex = metadata["/Signature"]
        digest_hex = metadata["/Digest"]

        content_bytes = b""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                content_bytes += text.encode('utf-8')

        digest = SHA256.new(content_bytes)

        if digest.hexdigest() != digest_hex: # compare the digest of the current content with the stored digest
            return False, "The PDF has been changed after signing!"

        signature = bytes.fromhex(signature_hex)

        with open(public_key_path, 'rb') as f:
            public_key = RSA.import_key(f.read())

        pkcs1_15.new(public_key).verify(digest, signature)
        return True, "Valid signature"
    except (ValueError, TypeError):
        return False, "Invalid signature"
    except Exception as e:
        return False, f"Error: {e}"
