import os
from typing import Optional
import typer
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.retrieval_qa.base import RetrievalQA

# Initialize Typer app for a professional CLI look
app = typer.Typer(help="CLI Chatbot")

def initialize_anant_rag(file_path: str):
    """Sets up the RAG engine using Groq and FAISS."""
    # 1. Load and Split Resume
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    anant_chunks = text_splitter.split_documents(documents)

    # 2. Create Embeddings (Local HuggingFace model is free and fast)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 3. Store in Vector DB
    vector_db = FAISS.from_documents(anant_chunks, embeddings)
    vector_db.save_local("faiss_index")
    
    # 4. Setup Groq LLM (LLaMA 3 70B for high-quality extraction)
    llm = ChatGroq(
        temperature=0.1,
        model_name="openai/gpt-oss-120b",
        groq_api_key=os.environ.get("GROQ_API_KEY")
    )

    # 5. Build Retrieval Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 8}),
    )
    
    return qa_chain
def formatted_response(text: str) -> str:
    return text.replace("**", "").strip()

@app.command()
def chat(resume_path: str = typer.Option(..., "--file", "-f", help="Path to the resume PDF")):
    """
    Start a conversation with the recruiter-facing chatbot.
    """
    if not os.environ.get("GROQ_API_KEY"):
        typer.echo("Error: Please set your GROQ_API_KEY environment variable.")
        raise typer.Exit()

    typer.secho(f"Initializing HireMe AI for: {resume_path}...", fg=typer.colors.CYAN)
    
    try:
        anant_bot = initialize_anant_rag(resume_path)
        typer.secho("System Ready. Recruiter, you may now ask questions about the candidate.", fg=typer.colors.GREEN)
        typer.echo("Type 'exit' or 'quit' to end the session.\n")
        conversation_history = []
        while True:
            query = typer.prompt("Recruiter")
            
            if query.lower() in ["exit", "quit"]:
                break
            conversation_history.append(f"Recruiter: {query}")
                
            prefix = (
    "You are a professional recruiter-facing assistant. "
    "Answer only based on the resume content provided. "
    "Always refer to the candidate in the third person. "
    "If the answer is not listed in the resume, say politely that it is not available. "
    "Maintain context of previous questions in the session. "
    "Respond in the same language as the question. "
    "Do not use markdown or tables. Return clean plain text.\n"
    "Question: "
    )            
            with typer.progressbar(length=100, label="Anant-Bot is thinking") as progress:
                full_prompt = prefix + "\n".join(conversation_history) + f"\nRecruiter: {query}"
                response = anant_bot.invoke(full_prompt)
                progress.update(100)
            answer = formatted_response(response['result'])
            conversation_history.append(f"AI: {answer}")
            typer.echo(f"\nAI: {answer}\n")
    except Exception as e:
        typer.secho(f"An error occurred: {e}", fg=typer.colors.RED)

if __name__ == "__main__":
    app()