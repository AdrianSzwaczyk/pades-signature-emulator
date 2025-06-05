from pypdf import PdfReader, PdfWriter
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

def sign_pdf(pdf_path, private_key_bytes):
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
