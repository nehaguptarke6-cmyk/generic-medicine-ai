from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS


def split_documents(documents):
    """
    Split documents into smaller chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(
        documents
    )

    return chunks


def create_vector_store(chunks, embeddings):
    """
    Create FAISS vector store.
    """

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store


def search_medicines(
    vector_store,
    query,
    k=3
):
    """
    Search medicines using semantic similarity.
    """

    results = vector_store.similarity_search(
        query,
        k=k
    )

    return results