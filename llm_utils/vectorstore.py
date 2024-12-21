import json
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Initialize ChromaDB client with persistence settings
client = chromadb.PersistentClient(path="../manu_db")
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def load_and_split_docs(doc_path: str):
    """
    Loads a DOC using Docx2txtLoader and splits the text into chunks.
    """
    loader = Docx2txtLoader(doc_path)
    documents = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    all_splits = text_splitter.split_documents(documents)
    return all_splits

def store_documents_in_db(docs, collection_name: str, base_id: str):
    """
    Store documents (split chunks) in the ChromaDB collection.
    """
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    # Create a collection named 'manu'
    collection = client.get_or_create_collection(name=collection_name)

    for i, doc in enumerate(docs):
        try:
            document_vector = embeddings.embed_documents([doc.page_content])

            # Ensure the vector was created correctly
            if not document_vector or len(document_vector[0]) == 0:
                print(f"Failed to embed document chunk {i} for {base_id}. Skipping...")
                continue

            doc_id = f"{base_id}_chunk_{i}"
            print(f"Storing document with ID: {doc_id} in {collection_name} collection")

            # Add the document chunk to the ChromaDB collection
            collection.add(
                documents=[doc.page_content],
                embeddings=document_vector,
                ids=[doc_id]
            )

        except Exception as e:
            print(f"Error processing document chunk {i} for {base_id}: {e}")


def split_and_store_doc(doc_path: str, base_id: str, collection: str):
    """
    Loads and splits a DOC, then stores it in ChromaDB.
    """
    try:
        splits = load_and_split_docs(doc_path)
        store_documents_in_db(splits, collection, base_id)
    except Exception as e:
        print(f"Error processing PDF {doc_path}: {e}")

def process_docs_in_directory(directory_path: str, collection: str):
    """
    Processes all PDF files in a specified directory and stores them in ChromaDB.
    """
    pdf_files = Path(directory_path).glob("*.docx")

    for pdf_file in pdf_files:
        base_id = pdf_file.stem
        print(f"Processing {pdf_file.name} with base ID: {base_id}")
        split_and_store_doc(pdf_file, base_id, collection)

def create_or_reset_vector_store():
    process_docs_in_directory("../data/Resume_Data", "resume")
    process_docs_in_directory("../data/Personality_Data", "personality")

if __name__ == "__main__":
    create_or_reset_vector_store()
