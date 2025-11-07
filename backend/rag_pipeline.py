import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

# Load environment variables (optional)
load_dotenv()

def build_rag_pipeline(document_text):
    """Builds a lightweight RAG (Retrieval-Augmented Generation) pipeline."""

    # 1️⃣ Split the document into small overlapping chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    texts = splitter.create_documents([document_text])

    # 2️⃣ Create vector embeddings for the text chunks
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(texts, embeddings)

    # 3️⃣ Use a small, CPU-friendly model
    generator = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        tokenizer="google/flan-t5-small",
        max_new_tokens=256,
        temperature=0.4,
        device=-1   # CPU mode
    )

    llm = HuggingFacePipeline(pipeline=generator)

    # 4️⃣ Combine retriever + LLM into a QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=False
    )

    return qa_chain
