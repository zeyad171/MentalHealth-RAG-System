# MentalHealth-RAG-System 🧠🔍

A Retrieval-Augmented Generation (RAG) system running on Google Gemini, providing medical manual-based mental health information with source-grounded, highly accurate responses.

## Overview ✨
This project implements an end-to-end RAG pipeline designed specifically for clinical and mental health guidelines. It extracts dense medical text, processes it into semantically meaningful chunks, and leverages vector similarity search to ground generative outputs in authoritative sources.

### Core Architecture

1. **📄 Document Ingestion**: Extracts raw text from medical manual PDFs.
2. **🧹 Preprocessing**: Cleans artifacts, regularizes formatting, and normalizes text.
3. **✂️ Semantic Chunking**: Splits text into 200-500 word context-aware segments.
4. **🧠 Embedding Generation**: Uses `all-MiniLM-L6-v2` (`sentence-transformers`) to convert text into high-dimensional vectors.
5. **🔍 Vector Search**: Stores and retrieves semantic chunks efficiently using FAISS (Facebook AI Similarity Search).
6. **⚙️ Generation**: Formulates grounded answers using Google Gemini's advanced LLM capabilities.

## Installation ⚙️

```bash
git clone https://github.com/zeyad171/MentalHealth-RAG-System.git
cd MentalHealth-RAG-System
pip install -r requirements.txt
```

## Setup & Usage 🚀

1. **Add Data**: Place your medical manual PDF inside the `data/` folder.
2. **Environment Variables**: Create a `.env` file in the root directory and add your credentials:
```bash
GEMINI_API_KEY="your_api_key"
PDF_PATH="data/manual.pdf"
```

3. **Run the Pipeline**:
Execute the main script to ingest the documents, build the vector index, and start the system:
```bash
python main.py
```

*Alternatively, if you only need to run the data cleaning pipeline:*
```bash
python cleaning.py data/manual.pdf
```

## Example Queries 💡

- *"What are the diagnostic criteria for PTSD?"*
- *"Explain the difference between bipolar I and II"*
- *"List autism spectrum disorder symptoms in adults"*

## Project Structure 📂
```bash
MentalHealth-RAG-System/
├── data/               # Medical manual PDF storage
├── main.py             # Main inference and execution pipeline
├── cleaning.py         # Advanced data cleaning and chunking script
├── Main.ipynb          # Jupyter notebook for interactive testing
├── cleaning.ipynb      # Jupyter notebook for interactive cleaning
├── requirements.txt    # Project dependencies
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation
```

## 🛠 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Gemini API errors** | Verify your API key at [Google AI Studio](https://aistudio.google.com/) and ensure the variable is saved in `.env`. |
| **FAISS loading errors** | Rebuild the vector store by deleting `faiss.index` and rerunning `main.py`. |
| **Missing dependencies** | Ensure all packages are installed via `pip install -r requirements.txt`. |

---
**Disclaimer** ⚠️: This tool provides informational content only and is not a substitute for professional medical advice.
