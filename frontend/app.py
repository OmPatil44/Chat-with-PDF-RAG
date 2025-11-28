import streamlit as st
from api_client import APIClient
import time

# --- Configuration ---
st.set_page_config(
    page_title="Research Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for "Less AI, More Professional" Look ---
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Theme Overrides */
    [data-testid="stAppViewContainer"] {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    p, div, span, label {
        font-family: 'Inter', sans-serif;
        color: #c9d1d9;
        line-height: 1.6;
    }
    code {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.9em;
    }

    /* Custom Header */
    .custom-header {
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #238636 0%, #2ea043 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
    }

    /* Buttons */
    .stButton > button {
        background-color: #238636;
        color: white;
        border: 1px solid rgba(240, 246, 252, 0.1);
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #2ea043;
        border-color: #8b949e;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: transparent;
        border: none;
        padding: 1.5rem 0;
    }
    [data-testid="stChatMessageContent"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Differentiate User vs Assistant */
    [data-testid="chatAvatarIcon-user"] {
        background-color: #238636;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #1f6feb;
    }
    
    /* Input Box */
    .stTextInput > div > div > input {
        background-color: #0d1117;
        border: 1px solid #30363d;
        color: #c9d1d9;
        border-radius: 8px;
        padding: 0.75rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3);
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #161b22;
        border: 1px dashed #30363d;
        border-radius: 8px;
        padding: 1rem;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #58a6ff;
    }

    /* Expander (Sources) */
    .streamlit-expanderHeader {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        color: #c9d1d9;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Style Header to match Dark Theme */
    header[data-testid="stHeader"] {
        background-color: #0d1117;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d1117; 
    }
    ::-webkit-scrollbar-thumb {
        background: #30363d; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #8b949e; 
    }
</style>
""", unsafe_allow_html=True)

# --- State Management ---
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

client = APIClient()

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #238636, #2ea043); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px;">R</div>
        <div>
            <h3 style="margin: 0; font-size: 1.2rem;">Research</h3>
            <p style="margin: 0; font-size: 0.8rem; opacity: 0.7;">Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Session Management
    st.markdown("### 💬 Session")
    if st.button("New Session", use_container_width=True):
        with st.spinner("Creating session..."):
            session = client.create_session()
            if session:
                st.session_state.session_id = session["session_id"]
                st.session_state.messages = []
                st.success("New session created!")
                time.sleep(1)
                st.rerun()
    
    if st.session_state.session_id:
        st.markdown(f"""
        <div style="background-color: #161b22; padding: 10px; border-radius: 6px; border: 1px solid #30363d; margin-top: 10px; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 0.8rem; color: #8b949e;">Active Session</p>
            <code style="color: #58a6ff;">{st.session_state.session_id[:8]}...</code>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📄 Documents")
        uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type="pdf")
        
        if uploaded_file:
            if st.button("Ingest Document", use_container_width=True):
                with st.spinner("Ingesting document..."):
                    result = client.upload_document(
                        st.session_state.session_id, 
                        uploaded_file, 
                        uploaded_file.name
                    )
                    if result:
                        st.success("Document ingested successfully!")
                    else:
                        st.error("Failed to ingest document.")
    else:
        st.info("Start a new session to begin.")
        
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #8b949e; font-size: 0.8rem;">
        <p>Powered by <strong>LangChain</strong> & <strong>Ollama</strong></p>
    </div>
    """, unsafe_allow_html=True)

# --- Main Chat Interface ---
if st.session_state.session_id:
    # Header
    st.markdown('<div class="custom-header">Research RAG Assistant</div>', unsafe_allow_html=True)
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_data = client.chat(st.session_state.session_id, prompt)
                
                if response_data:
                    ai_response = response_data["response"]
                    sources = response_data.get("sources", [])
                    
                    # Display response
                    st.markdown(ai_response)
                    
                    # Display sources if available
                    if sources:
                        with st.expander("📚 Sources"):
                            for idx, source in enumerate(sources):
                                st.markdown(f"**Source {idx+1}:** {source['source']}")
                                st.caption(source['page_content'])
                    
                    # Add AI message to state
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.error("Failed to get response from assistant.")
else:
    # Empty State with Hero Section
    st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; text-align: center;">
<div style="width: 80px; height: 80px; background: linear-gradient(135deg, #238636, #2ea043); border-radius: 20px; display: flex; align-items: center; justify-content: center; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(35, 134, 54, 0.3);">
<span style="font-size: 40px;">📚</span>
</div>
<h1 style="font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(90deg, #ffffff 0%, #c9d1d9 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Research RAG Assistant</h1>
<p style="font-size: 1.2rem; color: #8b949e; max-width: 600px; margin-bottom: 3rem;">
Your intelligent companion for analyzing research papers. Upload PDFs, ask complex questions, and get cited answers instantly.
</p>
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 900px; width: 100%;">
<div style="background-color: #161b22; padding: 2rem; border-radius: 12px; border: 1px solid #30363d;">
<div style="font-size: 2rem; margin-bottom: 1rem;">🚀</div>
<h3 style="font-size: 1.2rem; margin-bottom: 0.5rem;">Fast Ingestion</h3>
<p style="font-size: 0.9rem; color: #8b949e;">Process complex PDFs in seconds using local embeddings.</p>
</div>
<div style="background-color: #161b22; padding: 2rem; border-radius: 12px; border: 1px solid #30363d;">
<div style="font-size: 2rem; margin-bottom: 1rem;">🧠</div>
<h3 style="font-size: 1.2rem; margin-bottom: 0.5rem;">Smart Context</h3>
<p style="font-size: 0.9rem; color: #8b949e;">Retrieves only the most relevant sections for accurate answers.</p>
</div>
<div style="background-color: #161b22; padding: 2rem; border-radius: 12px; border: 1px solid #30363d;">
<div style="font-size: 2rem; margin-bottom: 1rem;">🔒</div>
<h3 style="font-size: 1.2rem; margin-bottom: 0.5rem;">Secure & Local</h3>
<p style="font-size: 0.9rem; color: #8b949e;">Your data stays on your machine. No external uploads required.</p>
</div>
</div>
<div style="margin-top: 3rem; animation: bounce 2s infinite;">
<p style="color: #58a6ff; font-weight: 500;">👈 Start by creating a New Session</p>
</div>
</div>
<style>
@keyframes bounce {
0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
40% {transform: translateY(-10px);}
60% {transform: translateY(-5px);}
}
</style>
""", unsafe_allow_html=True)
