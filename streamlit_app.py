import streamlit as st
import requests
import os

# Backend API URL Configuration
API_BASE_URL = os.getenv("DOCUMIND_API_URL", "http://127.0.0.1:8000")

# Streamlit Page Configuration
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    """Injects custom CSS for a modern, polished premium UI."""
    st.markdown("""
    <style>
    /* Global Background and Fonts */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom button hover styling */
    .stButton > button {
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
        border: 1px solid #e2e8f0;
    }
    
    .stButton > button:hover {
        border-color: #4f46e5;
        background-color: #f8fafc;
        color: #4f46e5;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.1);
    }
    
    /* Sidebar text color enforcement for Dark Sidebar */
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown h4,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown strong {
        color: #f8fafc !important;
    }
    
    /* Header styling */
    .main-header {
        color: #0f172a;
        font-weight: 700;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    .sub-header {
        color: #64748b;
        font-size: 1.15rem;
        font-weight: 500;
        margin-bottom: 25px;
    }
    
    /* Chat message container styling */
    .stChatMessage {
        border-radius: 12px;
        padding: 10px 15px;
        margin-bottom: 12px;
        background-color: transparent;
    }
    
    /* Answer Card Styling */
    .answer-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 24px;
        width: 100%;
    }
    
    .answer-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #4f46e5;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .answer-text {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1e293b;
        margin-bottom: 24px;
        white-space: pre-wrap;
    }
    
    .answer-meta {
        font-size: 0.9rem;
        color: #64748b;
        border-top: 1px solid #f1f5f9;
        padding-top: 12px;
        line-height: 1.5;
    }
    
    /* Expandable source cards */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 8px;
        color: #334155;
        font-weight: 600;
    }
    
    .source-meta-block {
        font-size: 0.9rem;
        color: #475569;
        margin-bottom: 12px;
        line-height: 1.5;
    }
    
    .source-text-block {
        font-size: 0.95rem;
        color: #334155;
        line-height: 1.6;
        background-color: #f8fafc;
        padding: 12px;
        border-left: 3px solid #6366f1;
        border-radius: 4px;
    }
    
    /* Status indicators */
    .status-online {
        color: #10b981;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 4px 10px;
        background-color: #d1fae5;
        border-radius: 12px;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    .status-offline {
        color: #ef4444;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 4px 10px;
        background-color: #fee2e2;
        border-radius: 12px;
        display: inline-block;
        margin-bottom: 15px;
    }
    
    /* Refined Premium Chat Input Styling */
    /* Blend the bottom sticky container into the main background */
    [data-testid="stBottomBlockContainer"] {
        background-color: #f8fafc !important;
        padding-bottom: 24px !important;
    }
    
    /* 1. Strip default backgrounds and borders from ALL Streamlit chat input elements */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div,
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="base-input"],
    [data-testid="stChatInput"] textarea,
    .stChatInputContainer {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* 2. Re-apply the premium styling ONLY to the MAIN wrapper */
    [data-testid="stChatInput"] > div {
        background-color: #ffffff !important;
        border: 1px solid #d9dee8 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.06) !important;
        transition: all 0.3s ease !important;
    }
    
    /* 3. Focus State */
    [data-testid="stChatInput"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.10), 0 4px 16px rgba(15, 23, 42, 0.06) !important;
    }
    
    /* 4. Input Field Fixes */
    [data-testid="stChatInput"] textarea {
        color: #1e293b !important; /* dark charcoal / slate */
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important; /* muted slate gray */
    }
    
    /* 5. Force identical Send Button styling in ALL states (empty, typing, active) */
    [data-testid="stChatInput"] button,
    [data-testid="stChatInput"] button:disabled,
    [data-testid="stChatInput"] button:not(:disabled),
    [data-testid="stChatInput"] button:hover,
    [data-testid="stChatInput"] button:focus,
    [data-testid="stChatInput"] button:active {
        background-color: transparent !important;
        color: #4f46e5 !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    [data-testid="stChatInput"] button svg,
    [data-testid="stChatInput"] button:disabled svg,
    [data-testid="stChatInput"] button:not(:disabled) svg {
        color: #4f46e5 !important;
        fill: #4f46e5 !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .answer-card {
            padding: 16px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def check_backend_health():
    """Checks if the FastAPI backend is responsive."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def ask_backend(question):
    """Sends a question to the FastAPI backend and retrieves the RAG response."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json={"question": question},
            timeout=180
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 422 or response.status_code == 400:
            return {"error": "Invalid request. Please provide a valid question."}
        else:
            return {"error": f"API Error: Server returned status code {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection Error: Unable to communicate with the backend. ({e})"}

def render_sidebar():
    """Renders the Streamlit sidebar."""
    with st.sidebar:
        st.markdown("### 🧠 DocuMind AI")
        st.markdown("---")
        
        st.markdown("#### 📚 Knowledge Base")
        st.markdown("**Agentic AI Executive Guide**")
        st.markdown("---")
        
        st.markdown("#### ⚙️ System Architecture")
        st.markdown("- **Embedding**: `all-MiniLM-L6-v2`")
        st.markdown("- **Vector Database**: `Qdrant`")
        st.markdown("- **LLM**: `Llama 3.2 3B`")
        st.markdown("- **Orchestration**: `LangGraph`")
        st.markdown("- **API**: `FastAPI`")
        st.markdown("---")
        
        st.markdown("#### ℹ️ About")
        st.markdown("DocuMind AI is a grounded RAG assistant designed to answer questions using **only** the provided Agentic AI knowledge base.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

def render_header():
    """Renders the application header and connection status."""
    st.markdown('<h1 class="main-header">🧠 DocuMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Grounded answers from your Agentic AI knowledge base</div>', unsafe_allow_html=True)
    
    is_online = check_backend_health()
    if is_online:
        st.markdown('<div class="status-online">● Backend Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-offline">● Backend Offline</div>', unsafe_allow_html=True)
        st.error(f"Unable to connect to the DocuMind AI backend.\n\nMake sure the FastAPI server is running at: `{API_BASE_URL}`")
        
    st.markdown("---")
    return is_online

def render_answer_card(answer, score, model, is_fallback=False):
    """Renders the single, dominant final answer card."""
    if is_fallback:
        st.markdown(f"""
        <div class="answer-card">
            <div class="answer-header">🤖 Final Answer</div>
            <div class="answer-text">{answer}</div>
        </div>
        """, unsafe_allow_html=True)
        st.info("No relevant information was found in the Agentic AI knowledge base.")
    else:
        st.markdown(f"""
        <div class="answer-card">
            <div class="answer-header">🤖 Final Answer</div>
            <div class="answer-text">{answer}</div>
            <div class="answer-meta">
                <strong>Top retrieval similarity:</strong> {score:.4f} <br>
                <strong>Model:</strong> {model}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_sources(retrieved_context):
    """Renders expandable source cards collapsed by default."""
    if not retrieved_context:
        return
        
    st.markdown("### Sources & Retrieved Context")
    st.markdown(f"*{len(retrieved_context)} retrieved chunks*")
    st.markdown("<br>", unsafe_allow_html=True)
    
    for idx, ctx in enumerate(retrieved_context):
        source = ctx.get("source", "Unknown")
        page = ctx.get("page", "N/A")
        chunk_id = ctx.get("chunk_id", "Unknown")
        score = ctx.get("score", 0.0)
        text = ctx.get("text", "")
        
        with st.expander(f"› 📄 {source} · Page {page} · Similarity {score:.4f}"):
            st.markdown(f"""
            <div class="source-meta-block">
                <strong>Source:</strong> {source} <br>
                <strong>Page:</strong> {page} <br>
                <strong>Chunk ID:</strong> {chunk_id} <br>
                <strong>Retrieval similarity:</strong> {score:.4f}
            </div>
            <strong>Retrieved context:</strong>
            <div class="source-text-block">{text}</div>
            """, unsafe_allow_html=True)

def initialize_session_state():
    """Initializes the required session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def handle_suggested_question(question):
    """Helper to inject a suggested question into the chat."""
    st.session_state.suggested_question = question

def main():
    inject_custom_css()
    initialize_session_state()
    render_sidebar()
    
    # Render the main header
    is_online = render_header()
    
    # Display the current conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(msg["content"])
            else:
                # Assistant message rendering with strong visual hierarchy
                is_fallback = msg.get("status") == "no_context"
                render_answer_card(
                    answer=msg["content"], 
                    score=msg.get("score"), 
                    model=msg.get("model"),
                    is_fallback=is_fallback
                )
                if msg.get("sources"):
                    render_sources(msg["sources"])
    
    # Empty State: Suggest questions to get started
    if not st.session_state.messages and is_online:
        st.markdown("### Suggested Questions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("What is Agentic AI?", use_container_width=True):
                handle_suggested_question("What is Agentic AI?")
        with col2:
            if st.button("What are AI agents?", use_container_width=True):
                handle_suggested_question("What are AI agents?")
        with col3:
            if st.button("What are the characteristics of Agentic AI systems?", use_container_width=True):
                handle_suggested_question("What are the characteristics of Agentic AI systems?")
    
    # Determine the query (from input box or a suggested button click)
    query = st.chat_input("Ask something about Agentic AI...", disabled=not is_online)
    if "suggested_question" in st.session_state:
        query = st.session_state.suggested_question
        del st.session_state.suggested_question
        
    if query:
        # Append and display the user's question
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
            
        # Display assistant loading state & fetch response
        with st.chat_message("assistant"):
            with st.spinner("Searching the knowledge base..."):
                response = ask_backend(query)
                
            if "error" in response:
                st.error(response["error"])
                st.session_state.messages.pop() # Remove the user query from history on error
                return
                
            status = response.get("status")
            answer = response.get("answer", "")
            sources = response.get("retrieved_context", [])
            score = response.get("retrieval_score")
            model = response.get("model", "llama3.2:3b")
            
            is_fallback = (status == "no_context")
            
            # Render to UI
            render_answer_card(answer, score, model, is_fallback=is_fallback)
            if not is_fallback:
                render_sources(sources)
                
            # Save to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources if not is_fallback else [],
                "score": score if not is_fallback else None,
                "model": model,
                "status": status
            })

if __name__ == "__main__":
    main()
