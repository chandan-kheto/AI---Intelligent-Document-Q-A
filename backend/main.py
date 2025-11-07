
from rag_pipeline import build_rag_pipeline
from utils.pdf_loader import extract_text_from_pdf

def run_rag(pdf_path, query):
    """Main RAG process"""
    print("🔍 Loading and embedding document...")
    document_text = extract_text_from_pdf(pdf_path)

    qa_chain = build_rag_pipeline(document_text)
    print("🤖 Generating response...")
    answer = qa_chain.run(query)
    return answer

if __name__ == "__main__":
    # Example test
    response = run_rag("AI note.pdf", "Explain NLP in simple terms.")

    print("Answer:", response)
