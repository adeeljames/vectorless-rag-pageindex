import os
from dotenv import load_dotenv
from pageindex import PageIndexClient
from src.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")

if not PAGEINDEX_API_KEY:
    logger.error("PAGEINDEX_API_KEY is not set in environment variables.")

# Initialize the PageIndex Client
pi_client = PageIndexClient(api_key=PAGEINDEX_API_KEY) if PAGEINDEX_API_KEY else None

def upload_document(file_path: str) -> str:
    """
    Uploads a document to PageIndex and returns the document ID.
    """
    if not pi_client:
        raise ValueError("PageIndex Client not initialized. Check API key.")
        
    try:
        logger.info(f"Submitting document to PageIndex: {file_path}")
        response = pi_client.submit_document(file_path)
        doc_id = response.get("doc_id")
        logger.info(f"Successfully submitted document. Doc ID: {doc_id}")
        return doc_id
    except Exception as e:
        logger.error(f"Error submitting document: {e}")
        raise

def get_document_status(doc_id: str) -> dict:
    """
    Checks the processing status of a document.
    """
    if not pi_client:
        raise ValueError("PageIndex Client not initialized. Check API key.")
        
    try:
        doc_info = pi_client.get_document(doc_id)
        return doc_info
    except Exception as e:
        logger.error(f"Error getting document status: {e}")
        raise

def chat_with_document_stream(query: str, doc_id: str):
    """
    Queries the document using PageIndex Chat API and yields the response stream.
    """
    if not pi_client:
        raise ValueError("PageIndex Client not initialized. Check API key.")
        
    try:
        logger.info(f"Sending query for doc_id {doc_id}:\n{query}")
        for chunk in pi_client.chat_completions(
            messages=[{"role": "user", "content": query}],
            doc_id=doc_id,
            stream=True
        ):
            yield chunk
    except Exception as e:
        logger.error(f"Error in chat completions stream: {e}")
        raise e
