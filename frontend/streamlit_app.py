import streamlit as st
import requests
import uuid

# ================= BACKEND URL (Ek Hi Jagah Change Karo) =================
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
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.all_chats[new_id] = {
        "title": "New Chat",
        "session_id": str(uuid.uuid4()),
        "history": []
    }
    st.session_state.current_chat_id = new_id

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("### 🤖 AI Assistant")
    st.markdown("---")

    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {
            "title": "New Chat",
            "session_id": str(uuid.uuid4()),
            "history": []
        }
        st.session_state.current_chat_id = new_id
        st.rerun()

    st.markdown("#### 📜 Chat History")

    for chat_id in reversed(list(st.session_state.all_chats.keys())):
        chat = st.session_state.all_chats[chat_id]
        label = chat["title"][:30] + ("..." if len(chat["title"]) > 30 else "")
        if st.button(f"💬 {label}", key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

    st.markdown("---")
    if st.button("🗑️ Delete Current Chat", use_container_width=True):
        current_id = st.session_state.current_chat_id
        session_id = st.session_state.all_chats[current_id]["session_id"]
        requests.delete(f"{BACKEND_URL}/history/{session_id}")
        del st.session_state.all_chats[current_id]
        if len(st.session_state.all_chats) == 0:
            new_id = str(uuid.uuid4())
            st.session_state.all_chats[new_id] = {
                "title": "New Chat",
                "session_id": str(uuid.uuid4()),
                "history": []
            }
            st.session_state.current_chat_id = new_id
        else:
            st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[0]
        st.rerun()

# ================= MAIN AREA =================
st.markdown('<p class="main-header">AI Research Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Document-grounded Q&A with real-time web search fallback</p>', unsafe_allow_html=True)
current_chat = st.session_state.all_chats[st.session_state.current_chat_id]

with st.expander("📄 Upload Document", expanded=False):
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        if st.button("Upload & Index Document"):
            with st.spinner("Uploading and indexing..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post(f"{BACKEND_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success("✅ Document uploaded and indexed successfully!")
                else:
                    st.error(f"Upload failed: {response.text}")

st.markdown("---")

for msg in current_chat["history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask a question...")

if query:
    if current_chat["title"] == "New Chat":
        current_chat["title"] = query[:40]

    current_chat["history"].append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/query",
                json={"query": query, "session_id": current_chat["session_id"]}
            )
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.markdown(answer)
                current_chat["history"].append({"role": "assistant", "content": answer})
            else:
                st.error(f"Query failed: {response.text}")

    st.rerun()