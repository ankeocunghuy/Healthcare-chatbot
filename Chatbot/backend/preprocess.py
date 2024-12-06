from pypdf import PdfReader

def preprocess_pdf(document):
    """# Preprocess pdf to text file """

    all_file = ""
    reader = PdfReader(document)
    for page in reader.pages:
        text = page.extract_text()
        all_file += text 
    return all_file

def create_documents(text, chunk_length):
    """# Split document to chunks with specific length """

    tokens = text.split()
    chunk = ""
    cur_len = 0
    docs = []
    for token in tokens:
        if cur_len == chunk_length:
            docs.append(chunk)
            chunk = ""
            cur_len = 0
        else:
            chunk += " "
            chunk += token
            cur_len += 1
    return docs

def create_documents_from_pdfs(pdf_files, chunk_length):
    """# Create documents from pdfs to list of strings with length chunklength"""

    docs = []
    
    for file in pdf_files:
        file_docs = create_documents(preprocess_pdf(file), chunk_length)
        docs += file_docs
    
    return docs


def load_guidelines(file_path):
    """# Read txt file"""
    with open(file_path, 'r') as file:
        return file.read()
    
def create_documents_from_txts(file_path):
    """# Create document from pdf """
    guidelines_text = load_guidelines(file_path)
    return guidelines_text.split("\n\n")