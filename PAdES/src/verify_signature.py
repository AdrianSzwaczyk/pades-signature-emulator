from pypdf import PdfReader
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def verify_pdf_signature(pdf_path, public_key_path):
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
