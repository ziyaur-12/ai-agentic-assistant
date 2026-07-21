import streamlit as st
import requests
import uuid

# ================= BACKEND URL (Ek Hi Jagah Change Karo) =================
# BACKEND_URL = "http://127.0.0.1:8000"
BACKEND_URL = "https://ai-agentic-assistant.onrender.com"

st.set_page_config(page_title="AI Research Assistant", page_icon="🤖", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    :root { color-scheme: dark; }

    header[data-testid="stHeader"] { background: #0d1117 !important; }
    footer {visibility: hidden;}
    .stApp { background-color: #0d1117 !important; }

    .main-header {
        color: #e6edf3 !important;
        font-size: 1.9rem;
        font-weight: 700;
        padding: 4px 0;
        border-bottom: 1px solid #21262d;
        margin-bottom: 4px;
    }
    .sub-header {
        color: #7d8590 !important;
        font-size: 0.9rem;
        margin-bottom: 24px;
    }

    section[data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #21262d;
    }

    .stApp * {
        color: #e6edf3 !important;
    }

    .stChatMessage {
        background-color: #161b22 !important;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }
    .stChatMessage strong { color: #58a6ff !important; }
    .stChatMessage h1, .stChatMessage h2, .stChatMessage h3, .stChatMessage h4 {
        color: #58a6ff !important;
    }

    .stButton button, .stFileUploader button, .stChatInput button {
        background-color: #21262d !important;
        color: #e6edf3 !important;
        border-radius: 6px;
        border: 1px solid #30363d !important;
    }
    .stButton button:hover, .stFileUploader button:hover {
        background-color: #30363d !important;
        border: 1px solid #58a6ff !important;
    }
    .stButton button *, .stFileUploader button * {
        color: #e6edf3 !important;
        fill: #e6edf3 !important;
    }

    div[data-testid="stSidebar"] .stButton:first-of-type button {
        background-color: #1f6feb !important;
        border: none !important;
    }
    div[data-testid="stSidebar"] .stButton:first-of-type button * {
        color: white !important;
    }

    .stFileUploader section {
        background-color: #161b22 !important;
        border: 1px dashed #30363d !important;
    }
    .stFileUploader section * {
        color: #e6edf3 !important;
    }

    .stChatInput textarea {
        border-radius: 8px !important;
        border: 1px solid #30363d !important;
        background-color: #161b22 !important;
        color: #e6edf3 !important;
    }
    div[data-testid="stBottom"], div[data-testid="stBottomBlockContainer"] {
        background-color: #0d1117 !important;
    }
    .stChatInput button {
        background-color: #1f6feb !important;
    }
    .stChatInput button svg { fill: white !important; }

    details {
        background-color: #161b22 !important;
        border: 1px solid #21262d !important;
        border-radius: 8px !important;
    }
    details summary {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
    }
    details summary * {
        color: #e6edf3 !important;
        fill: #e6edf3 !important;
    }
    details[open] summary {
        border-bottom: 1px solid #21262d !important;
    }

    .stAlert { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE SETUP =================
if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.current_session_id = new_id
    st.session_state.current_history = []

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("### 🤖 AI Assistant")
    st.markdown("---")

    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.current_chat_id = new_id
        st.session_state.current_session_id = new_id
        st.session_state.current_history = []
        st.rerun()

    st.markdown("#### 📜 Chat History")

    # Backend se saari saved chats fetch karo
    try:
        sessions_response = requests.get(f"{BACKEND_URL}/sessions", timeout=10)
        saved_sessions = sessions_response.json().get("sessions", []) if sessions_response.status_code == 200 else []
    except requests.exceptions.RequestException:
        saved_sessions = []

    for session in saved_sessions:
        label = session["title"][:30] + ("..." if len(session["title"]) > 30 else "")
        if st.button(f"💬 {label}", key=session["session_id"], use_container_width=True):
            st.session_state.current_chat_id = session["session_id"]
            st.session_state.current_session_id = session["session_id"]
            # Backend se poori history fetch karo
            try:
                hist_response = requests.get(f"{BACKEND_URL}/history/{session['session_id']}", timeout=10)
                st.session_state.current_history = hist_response.json().get("history", [])
            except requests.exceptions.RequestException:
                st.session_state.current_history = []
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Delete Current Chat", use_container_width=True):
        session_id = st.session_state.get("current_session_id")
        if session_id:
            requests.delete(f"{BACKEND_URL}/history/{session_id}")
        new_id = str(uuid.uuid4())
        st.session_state.current_chat_id = new_id
        st.session_state.current_session_id = new_id
        st.session_state.current_history = []
        st.rerun()

# ================= MAIN AREA =================
st.markdown('<p class="main-header">AI Research Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Document-grounded Q&A with real-time web search fallback</p>', unsafe_allow_html=True)
current_session_id = st.session_state.current_session_id
current_history = st.session_state.current_history

with st.expander("📄 Upload Document", expanded=False):
   uploaded_files = st.file_uploader("Choose documents (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    if st.button("Upload & Index Document(s)"):
        for uploaded_file in uploaded_files:
            with st.spinner(f"Uploading {uploaded_file.name}..."):
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{BACKEND_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success(f"✅ {uploaded_file.name} uploaded and indexed!")
                else:
                    st.error(f"Upload failed for {uploaded_file.name}: {response.text}")

st.markdown("---")

for msg in current_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask a question...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": query, "session_id": current_session_id}
            )
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.markdown(answer)

                # Backend se updated history fetch karo taaki session_state sync rahe
                try:
                    hist_response = requests.get(f"{BACKEND_URL}/history/{current_session_id}", timeout=10)
                    st.session_state.current_history = hist_response.json().get("history", [])
                except requests.exceptions.RequestException:
                    pass
            else:
                st.error(f"Query failed: {response.text}")

    st.rerun()