import os
import re
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: GEMINI_API_KEY not found in .env")

# Initialize models
model = genai.GenerativeModel("gemini-2.0-flash")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ''
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text() + '\n'
    return full_text

def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
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

def setup_rag(pdf_path):
    print(f"Reading {pdf_path}...")
    try:
        raw_text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None, None
        
    print("Cleaning text...")
    cleaned_text = clean_text(raw_text)
    
    print("Chunking text...")
    chunks = chunk_text(cleaned_text)
    
    print("Creating embeddings (this may take a moment)...")
    embeddings = embed_model.encode(chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    
    print("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, chunks

def retrieve_top_chunks(query, embed_model, index, chunks, top_k=5):
    query_embedding = embed_model.encode([query])[0].astype('float32')
    distances, indices = index.search(np.array([query_embedding]), top_k)
    return [chunks[i] for i in indices[0]]

def generate_with_gemini(question, context):
    prompt = f"""You are a helpful assistant with access to medical manual knowledge.

Answer the following question based on the context below.

Context:
{context}

Question:
{question}

Answer:"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return None

if __name__ == "__main__":
    pdf_path = os.getenv("PDF_PATH", "data/manual.pdf")
    if not os.path.exists(pdf_path):
        print(f"Please place your PDF at {os.path.abspath(pdf_path)}")
    else:
        index, chunks = setup_rag(pdf_path)
        if index is not None and chunks is not None:
            print("\nSetup complete! You can now start asking questions.")
            while True:
                q = input("\nAsk a question (or type 'quit' to exit): ")
                if q.lower() in ['quit', 'exit', 'q']:
                    break
                print("\nRetrieving context...")
                top_chunks = retrieve_top_chunks(q, embed_model, index, chunks)
                context = "\n\n".join(top_chunks)
                
                print("Generating answer...")
                ans = generate_with_gemini(q, context)
                if ans:
                    print("\nAnswer:\n", ans)
                else:
                    print("\nFailed to generate an answer.")
