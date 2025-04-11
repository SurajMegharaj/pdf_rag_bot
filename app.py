import streamlit as st
import requests

# ---- Configuration ----
st.set_page_config(page_title="PDF Chatbot", page_icon="🤖", layout="wide")

UPLOAD_API_URL = "http://localhost:8000/upload"  # FastAPI endpoint for file upload
ASK_API_URL = "http://localhost:8001/ask"         # FastAPI endpoint for query asking

# ---- Session State Initialization ----
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- Functions ----
def show_upload_popup():
    st.sidebar.header("📎 Attach your PDF")
    username = st.sidebar.text_input("Username", key="username_input")
    file = st.sidebar.file_uploader("Upload PDF", type=["pdf"], key="file_uploader")

    if st.sidebar.button("Upload and Load"):
        if username and file:
            files = {"file": (file.name, file, "application/pdf")}
            data = {"username": username}
            response = requests.post(UPLOAD_API_URL, files=files, data=data)

            if response.status_code == 200:
                st.success("✅ File uploaded successfully!")
                st.session_state.uploaded = True
                st.session_state.username = username
                st.session_state.chat_history = []  # Clear previous chats
            else:
                st.error("❌ Upload failed. Please try again.")
        else:
            st.warning("⚠️ Both username and file are required!")

def send_message(user_message):
    payload = {
        "username": st.session_state.username,
        "query": user_message
    }
    response = requests.post(ASK_API_URL, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result.get("response", "No response found.")
    else:
        return "Error communicating with server."

# ---- UI Layout ----
show_upload_popup()

st.title("🤖 PDF Chatbot")

# If file uploaded, show chat input
if st.session_state.uploaded:
    # Display chat history
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Chat input
    user_query = st.chat_input("Ask a question about your PDF...")
    if user_query:
        # Add user query to history
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        # Send to backend
        bot_response = send_message(user_query)

        # Add bot response to history
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

        # Re-render
        st.experimental_rerun()
else:
    st.info("👆 Attach your data first to start chatting!")
