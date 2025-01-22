import streamlit as st
from agents import graph
import os

def generate_response(input_text):
    for s in graph.stream({"messages": [("user",input_text)]}, subgraphs=True):
        # st.info(s)
        # print(s)
        # print("----")
        if list(s[1])[0] == 'supervisor':
            print(s)
            if list(s[1].values())[0]['next'] != '__end__':
                st.info(f"""SUPERVISOR: Reviewing prompt with AI Agents...""".format())
            else:
                st.info("SUPERVISOR: Agents have completed your propmt request.")
                if os.path.exists("data/output.txt"):
                    with open("data/output.txt", "rb") as file:
                        st.download_button(
                            label="Download article search results",
                            data=file,
                            file_name='search_results.txt',
                            mime="text/csv"
                        )
                    st.info("SUPERVISOR: You can find their findings in the file attached")
                    os.remove("data/output.txt")
                # uploaded_file = st.file_uploader("Choose a file")
                # if uploaded_file is not None:
                #     st.info("SUPERVISOR: You can find their findings in the file attached")
                #     bytes_data = uploaded_file.read()
                #     st.write("filename:", uploaded_file.name)
                #     st.write(bytes_data)
                #     os.remove("data/output.txt")
        elif ('agent' in list(s[1])[0]) and not(isinstance(list(s[1].values())[0]['messages'][0].content, list)):
            message_info = list(s[1].values())[0]['messages'][0]
            #print(message_info.name.format(), ":")
            print(s)
            print("-----"*20)
            ai_name = message_info.name
            if ai_name == None:
                ai_name = s[0][0].split(":")[0]
            ai_msg = message_info.content
            st.info(f"""{ai_name.upper()}:\n {ai_msg}""")
        else:
            message_info = list(s[1].values())[0]['messages'][0]
            print(message_info.content)
            print("-----"*20)

def init_chat():
    """Initialize chat session state with specific agent ID"""
    # Always reinitialize messages when switching agents
    st.session_state.messages = []

def show_chat(prompt_placeholder: str = "Ask me to pull an article!", extra_info: str = ""):
    st.markdown("---")
    st.subheader("Chat with an AI Team!")


    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"].split("*&()")[0])
    
    # Chat input
    if prompt := st.chat_input(prompt_placeholder):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt + f"*&() Use this extra information to provide better context and details: {extra_info}"})
        with st.chat_message("user"):
            st.markdown(prompt)

        #st.st

        with st.chat_message("my_form"):
            #submitted = st.form_submit_button("Submit")
            st.session_state.messages.append({"role": "assistant", "content": prompt})
            generate_response(prompt)