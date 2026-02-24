import streamlit as st
import os
import time
from src.rag_api import upload_document, get_document_status, chat_with_document_stream

st.set_page_config(page_title="PageIndex Agentic RAG", page_icon="🤖", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 5px;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4B5563;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🤖 PageIndex Agentic RAG</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload your document and chat with it instantly using reasoning-based RAG.</p>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "doc_id" not in st.session_state:
    st.session_state.doc_id = None

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        if "last_uploaded_name" not in st.session_state or st.session_state.last_uploaded_name != uploaded_file.name:
            # We have a new file
            st.session_state.doc_id = None
            st.session_state.messages = []
            st.session_state.last_uploaded_name = uploaded_file.name
            
            with st.spinner("Uploading and processing document (This may take a minute)..."):
                # Save file temporarily
                temp_dir = "temp_data"
                os.makedirs(temp_dir, exist_ok=True)
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Upload to PageIndex
                try:
                    doc_id = upload_document(temp_path)
                    
                    # Wait for processing
                    status = "processing"
                    prog_bar = st.progress(0, text="Processing document...")
                    while status == "processing":
                        info = get_document_status(doc_id)
                        status = info.get("status", "processing")
                        if status == "processing":
                            time.sleep(2)
                            
                    prog_bar.empty()
                    
                    if status == "completed":
                        st.session_state.doc_id = doc_id
                        st.success("✨ Document processed successfully!")
                    else:
                        st.error(f"Document failed to process. Status: {status}")
                except Exception as e:
                    st.error(f"Error processing document: {e}")
                finally:
                    # Clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
    if st.session_state.doc_id:
        st.success(f"Active Document ID: {st.session_state.doc_id}")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your document"):
    if not st.session_state.doc_id:
        st.warning("⚠️ Please upload a document first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Stream the response chunk by chunk
                for chunk in chat_with_document_stream(prompt, st.session_state.doc_id):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                full_response = "Sorry, I encountered an error while fetching the response."
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})
