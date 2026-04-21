import PyPDF2

def readPdfText(uploaded_file):
    text = ""

    # uploaded_file is already a file-like object
    reader = PyPDF2.PdfReader(uploaded_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text