# Resume Chatbot

A simple CLI-based AI assistant that allows recruiters to interact with a candidate’s resume using natural language.

The system uses Retrieval-Augmented Generation (RAG) to ensure responses are grounded strictly in the resume content.

---

## What This Project Does

- Reads a resume (PDF)
- Breaks it into chunks
- Stores embeddings using FAISS
- Retrieves relevant information based on user queries
- Uses an LLM to generate accurate, grounded responses

You can ask things like:
- "What are Anant’s qualifications?"
- "Does he have experience in AI?"
- "anant kaha rehta hai"

---

## Key Features

- Grounded answers (no hallucination)
- Context-aware conversation
- Works in both English and Hindi
- Clean, recruiter-friendly responses
- CLI-based interface using Typer

---

## Tech Stack

- Python
- LangChain
- FAISS (Vector Database)
- HuggingFace Embeddings
- Groq LLM
- Typer (CLI)

---

## Setup Instructions

### 1. Create Virtual Environment
python -m venv anant_env
anant_env\Scripts\activate

---

### 2. Install Dependencies
pip install typer langchain langchain-community langchain-huggingface sentence-transformers pypdf faiss-cpu

---

### 3. Set API Key

Set your Groq API key:

Windows:
set GROQ_API_KEY=your_key_here

---

### 4. Run the Project

python main.py --file "path_to_resume.pdf"

---

## How It Works

1. Resume is loaded using PyPDFLoader
2. Text is split into smaller chunks
3. Each chunk is converted into embeddings
4. Stored in FAISS vector database
5. On query:
   - Relevant chunks are retrieved
   - LLM generates answer based only on those chunks

---

## Important Design Decisions

### Why FAISS?
Even though we store conversation history, FAISS is used to:
- Retrieve only relevant parts of the resume
- Avoid sending entire document to LLM
- Improve accuracy and reduce cost

---

### Why Conversation History?
- Enables follow-up questions
- Maintains context across queries

---

### Why "Strict Grounding"?
To ensure:
- No hallucinated answers
- Only resume-based responses
- Professional reliability
