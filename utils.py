from pypdf import PdfReader
import io

def extract_pdf_text(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))  # wrap bytes in stream
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ''
    return text
