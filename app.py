"""
GenAI RAG Assistant - powered by Google Gemini
------------------------------------------------
Upload a PDF, ask questions about it. Uses:
  - Google Gemini (via langchain-google-genai) for chat responses
  - Google's embedding model for turning text into vectors
  - An in-memory vector store for retrieval (no extra DB setup needed)

Run with:
    streamlit run rag_assistant.py
"""

import os
import streamlit as st
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# ---------------------------------------------------------------------------
# Basic styling (dark theme, matches the original DeepSeek UI)
# ---------------------------------------------------------------------------
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stChatInput input {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #3A3A3A !important;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #1E1E1E !important;
        border: 1px solid #3A3A3A !important;
        border-radius: 10px; padding: 15px; margin: 10px 0;
    }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #2A2A2A !important;
        border: 1px solid #404040 !important;
        border-radius: 10px; padding: 15px; margin: 10px 0;
    }
    h1, h2, h3 { color: #00FFAA !important; }
    </style>
""", unsafe_allow_html=True)

PROMPT_TEMPLATE = """
You are an expert research assistant. Use the provided context to answer the query.
If the answer isn't in the context, say you don't know — do not make something up.
Be concise and factual (max 4 sentences).

Query: {user_query}
Context: {document_context}
Answer:
"""

PDF_STORAGE_PATH = "document_store/pdfs/"
os.makedirs(PDF_STORAGE_PATH, exist_ok=True)

# ---------------------------------------------------------------------------
# Sidebar: Google API key + model choice
# ---------------------------------------------------------------------------
st.sidebar.header("⚙️ Configuration")

# Key resolution order:
#   1. Streamlit secrets (used automatically on Streamlit Community Cloud,
#      or locally if you create .streamlit/secrets.toml)
#   2. Manual paste in the sidebar (used for quick local testing)
try:
    api_key = st.secrets.get("GOOGLE_API_KEY", "")
except Exception:
    api_key = ""

if api_key:
    st.sidebar.success("API key loaded from secrets.")
else:
    api_key = st.sidebar.text_input(
        "Google API Key",
        type="password",
        help="Get a free key at https://aistudio.google.com/apikey"
    )

selected_model = st.sidebar.selectbox(
    "Choose Gemini model",
    ["gemini-1.5-flash", "gemini-1.5-pro"],
    index=0,
    help="flash = faster & free-tier friendly. pro = higher quality, lower free-tier limits."
)

st.sidebar.divider()
st.sidebar.markdown("### Capabilities")
st.sidebar.markdown("""
- 📄 PDF document Q&A
- 🔍 Semantic search over your document
- 💬 Chat-style interface
""")

if not api_key:
    st.sidebar.warning("Paste your Google API key above to enable the assistant.")

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title("📘 GenAI RAG Assistant")
st.caption("Ask questions about your PDF, answered using Google Gemini.")
st.markdown("---")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(PDF_STORAGE_PATH, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def load_pdf_documents(file_path):
    return PDFPlumberLoader(file_path).load()


def chunk_documents(raw_documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    return splitter.split_documents(raw_documents)


def get_vector_store(api_key):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=api_key
    )
    return InMemoryVectorStore(embeddings)


def generate_answer(user_query, context_documents, api_key, model_name):
    context_text = "\n\n".join(doc.page_content for doc in context_documents)
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatGoogleGenerativeAI(
        model=model_name, google_api_key=api_key, temperature=0.3
    )
    chain = prompt | llm
    response = chain.invoke({"user_query": user_query, "document_context": context_text})
    return response.content


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "message_log" not in st.session_state:
    st.session_state.message_log = []

# ---------------------------------------------------------------------------
# File upload + indexing
# ---------------------------------------------------------------------------
uploaded_pdf = st.file_uploader(
    "Upload a PDF document",
    type="pdf",
    help="Select a PDF to ask questions about"
)

if uploaded_pdf and api_key:
    with st.spinner("Reading and indexing document..."):
        try:
            saved_path = save_uploaded_file(uploaded_pdf)
            raw_docs = load_pdf_documents(saved_path)
            chunks = chunk_documents(raw_docs)
            store = get_vector_store(api_key)
            store.add_documents(chunks)
            st.session_state.vector_store = store
            st.success(f"✅ Indexed {len(chunks)} chunks from '{uploaded_pdf.name}'. Ask away below.")
        except Exception as e:
            st.error(f"Failed to process document: {e}")
elif uploaded_pdf and not api_key:
    st.warning("Enter your Google API key in the sidebar before uploading.")

# ---------------------------------------------------------------------------
# Chat interface
# ---------------------------------------------------------------------------
for message in st.session_state.message_log:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_query = st.chat_input("Ask a question about the document...")

if user_query:
    if not api_key:
        st.error("Please enter your Google API key in the sidebar first.")
    elif st.session_state.vector_store is None:
        st.error("Please upload and index a PDF first.")
    else:
        st.session_state.message_log.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.spinner("Thinking..."):
            try:
                relevant_docs = st.session_state.vector_store.similarity_search(user_query, k=4)
                answer = generate_answer(user_query, relevant_docs, api_key, selected_model)
            except Exception as e:
                answer = f"Error calling Gemini API: {e}"

        st.session_state.message_log.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

if st.button("Clear Chat History"):
    st.session_state.message_log = []
    st.rerun()
