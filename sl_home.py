import streamlit as st
from chat import init_chat, show_chat


def init_session_state():
    """Initialize session state variables"""
    # Initialize chat with home page agent
    
    init_chat()

def main():
    st.title("Pull Scientific Articles")
    st.write("Welcome and meet your team of Agents to help look at articles")
    # Initialize session state
    init_session_state()
    
    # Show features
    st.subheader("Prompt Help")
    st.write("""
    - 📚 **Prompt Example**: Get me a list of research papers on the topic Prompt Compression
    """)
    
    # Show chat interface
    show_chat("Hi! I'm your AI Agent Manager. How can I help you today?")

if __name__ == "__main__":
    main()