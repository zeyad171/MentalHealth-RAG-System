import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ''
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text() + '\n'
    return full_text

def extract_text_from_txt(txt_path):
    with open(txt_path, "r", encoding="utf-8") as file:
        full_text = file.read()
    return full_text

def clean_text(text):
    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    # Remove multiple newlines and excess whitespace
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)

    # Remove standalone numbers (common in reference lists and section markers)
    text = re.sub(r'\b\d+\b', '', text)

    # Remove lines that likely contain author names or affiliations (e.g., 'Dr. John Smith', 'APA', etc.)
    text = re.sub(r'(Dr\.|Professor|MD|PhD|APA|American Psychiatric Association)[^\n]*\n', '', text, flags=re.IGNORECASE)

    # Remove reference styles like [1], (1), etc.
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\(\d+\)', '', text)

    # Optional: Remove page numbers if structured like 'Page 123'
    text = re.sub(r'Page\s*\d+', '', text, flags=re.IGNORECASE)

    # Optional: Remove any remaining overly short lines
    text = '\n'.join([line for line in text.splitlines() if len(line.strip()) > 20])

    return text.strip()

def chunk_text(text, min_words=200, max_words=500):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        end = i + max_words
        chunk = words[i:end]
        if len(chunk) >= min_words:
            chunks.append(" ".join(chunk))
        i += max_words
    return chunks

if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) < 2:
        print("Usage: python cleaning.py <path_to_pdf_or_txt>")
        sys.exit(1)

    input_path = sys.argv[1]
    
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        sys.exit(1)

    print(f"Reading {input_path}...")
    if input_path.lower().endswith('.pdf'):
        raw_text = extract_text_from_pdf(input_path)
    else:
        raw_text = extract_text_from_txt(input_path)

    with open("manual_raw.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)
    print("Saved 'manual_raw.txt'")

    print("Cleaning text...")
    cleaned_text = clean_text(raw_text)

    with open("manual_cleaned.txt", "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print("Saved 'manual_cleaned.txt'")

    print("Chunking text...")
    chunks = chunk_text(cleaned_text)

    with open("manual_chunks.txt", "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"--- Chunk {i+1} ---\n{chunk}\n\n")
    print("Saved 'manual_chunks.txt'")
    print("Cleaning and chunking complete!")
