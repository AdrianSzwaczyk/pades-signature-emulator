"""!
@file sign_pdf.py
@brief Contains the function to sign a PDF file using a private RSA key.
"""

from pypdf import PdfReader, PdfWriter
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

def sign_pdf(pdf_path, private_key_bytes):
    """! 
    @brief Function is responsible for signing a PDF file using a private RSA key.

    @details This function opens and reads the PDF file with use of pypdf library, extracts text from each page and computes the SHA256 digest of the content.
    Later, the signature is created using the private key and the digest. Those data is then added to the PDF metadata as "/Signature" and "/Digest". Additionally,
    the "/SignedBy" field is added with a value "User A". Finally, the signed PDF is saved to a new file with "_signed" suffix.
    The function uses the following libraries: 
    - 'pypdf' for PDF parsing
    - Crypto.Hash.SHA256, Crypto.Signature.pkcs1_15, and Crypto.PublicKey.RSA from the 'pycryptodome' package for cryptographic operations.


    @param pdf_path (str)  The path to the PDF file to verify.
    @param public_key_path (str)  The path to the public key file in .PEM format.

    @return  bool: Returns True if the signing was successful, False otherwise.
    """
    try:
        key = RSA.import_key(private_key_bytes)
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        content_bytes = b""
        for page in reader.pages:
            writer.add_page(page)
            text = page.extract_text()
            if text:
                content_bytes += text.encode('utf-8')

        digest = SHA256.new(content_bytes) # digest - SHA256 hash of the PDF content
        signature = pkcs1_15.new(key).sign(digest) # RSA signature of the digest

        writer.add_metadata({
            "/SignedBy": "User A",
            "/Signature": signature.hex(),
            "/Digest": digest.hexdigest()
        })

        output_path = pdf_path.replace(".pdf", "_signed.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

        return True
    except Exception as e:
        print(f"[sign_pdf] Error: {e}")
        return False
