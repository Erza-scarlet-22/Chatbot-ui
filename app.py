import streamlit as st
from datetime import datetime

def main():
    st.set_page_config(page_title="Ingram Micro Chat", layout="wide")

    # Custom CSS for blue color scheme and cyan sidebar
    st.markdown("""
    <style>
    .stApp {
        background-color: #E6F3FF;
    }
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
    }
    .stButton > button {
        background-color: #0088CC;
        color: white;
    }
    .css-1d391kg {  /* This class targets the sidebar */
        background-color: #00FFFF;
    }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.title("Ingram Micro Chat")

    # Sidebar
    st.sidebar.title("Chat Options")
    doc_choice = st.sidebar.radio(
        "Choose document to chat with:",
        ("Palo Alto Docs", "OneNote Docs")
    )

    # File upload button in sidebar
    uploaded_file = st.sidebar.file_uploader("Upload a file", type=["txt", "pdf", "doc", "docx"])
    if uploaded_file is not None:
        st.sidebar.success(f"File {uploaded_file.name} uploaded successfully!")

    # Previous chat history in sidebar
    st.sidebar.subheader("Previous Chats")
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    for idx, chat in enumerate(st.session_state.chat_history):
        if st.sidebar.button(f"Chat {idx + 1}: {chat['time']}", key=f"chat_{idx}"):
            st.session_state.current_chat = idx

    # New chat button
    if st.sidebar.button("Start New Chat"):
        st.session_state.chat_history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "messages": []})
        st.session_state.current_chat = len(st.session_state.chat_history) - 1

    # Main chat area
    st.header(f"Chat with {doc_choice}")

    # Display current chat
    if 'current_chat' in st.session_state:
        for message in st.session_state.chat_history[st.session_state.current_chat]['messages']:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to current chat
        if 'current_chat' not in st.session_state:
            st.session_state.chat_history.append({"time": datetime.now().strftime("%Y-%m-%d %H:%M"), "messages": []})
            st.session_state.current_chat = len(st.session_state.chat_history) - 1
        
        st.session_state.chat_history[st.session_state.current_chat]['messages'].append({"role": "human", "content": user_input})
        
        with st.chat_message("human"):
            st.write(user_input)
        
        # Here you would typically process the input and generate a response
        # For this example, we'll just echo the input
        ai_response = f"You said: {user_input}"
        st.session_state.chat_history[st.session_state.current_chat]['messages'].append({"role": "ai", "content": ai_response})
        
        with st.chat_message("ai"):
            st.write(ai_response)

if __name__ == "__main__":
    main()
