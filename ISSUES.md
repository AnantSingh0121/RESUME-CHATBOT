# Issues Faced & How They Were Solved

## 1. Missing Dependencies Errors
While running the project, multiple import errors appeared:
- typer not found
- langchain modules missing
- pypdf and sentence-transformers not installed

### Fix
Installed required dependencies step by step using pip:
pip install typer langchain langchain-community langchain-huggingface sentence-transformers pypdf faiss-cpu

---

## 2. LangChain Import Breaking Changes
The older import:
from langchain.chains import RetrievalQA

was not working due to version changes.

### Fix
Used updated import:
from langchain_classic.chains.retrieval_qa.base import RetrievalQA

---

## 3. CLI Command Not Working
Command:
python main.py chat --file resume.pdf

was throwing:
"unexpected extra argument (chat)"

### Fix
Adjusted usage to:
python main.py --file resume.pdf

and ensured @app.command() is correctly defined.

---

## 4. Resume Data Not Being Retrieved (RAG Issue)
Even though "Mumbai" was present in the resume, the bot failed to answer location-based queries.

### Root Cause
Top-K retrieval was too low and chunking was not optimal.

### Fix
- Increased retrieval depth:
  k=8
  
---

## 5. Context Not Maintained
Follow-up questions were not understood.

### Fix
Introduced conversation history:
- Stored previous Q&A
- Passed into prompt every time

---

## 6. Prompt Not Passing Current Query Properly
The latest user query was not always included correctly.

### Fix
Constructed full prompt like:
prefix + history + current query