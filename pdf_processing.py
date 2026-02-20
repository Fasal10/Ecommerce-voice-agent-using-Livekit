import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def create_vector_db():
    # 1. Define absolute paths
    # Using raw strings (r"...") to handle Windows backslashes correctly
    pdf_path = r"C:\Users\fasal_pgbi6fg\OneDrive\Desktop\Ecommerce-bot\pdf\ecommerce_bot.pdf"
    vector_db_path = r"C:\Users\fasal_pgbi6fg\OneDrive\Desktop\Ecommerce-bot\vector_db"

    # Check if PDF exists before proceeding
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return

    # 2. Load the PDF
    print(f"Loading PDF from: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    # 3. Chunk the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    chunks = text_splitter.split_documents(pages)
    
    print(f"Split {len(pages)} pages into {len(chunks)} chunks.")

    # 4. Create Embeddings and Store in FAISS
    print("Creating embeddings...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embeddings)

    # 5. Save the vector store to the specific folder
    print(f"Saving vector database to: {vector_db_path}")
    vector_store.save_local(vector_db_path)
    print("Vector database creation complete.")

if __name__ == "__main__":
    create_vector_db()