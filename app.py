import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
import re

title = "GPTBox"
st.set_page_config(page_title=title, layout="wide", initial_sidebar_state="expanded")

hide_streamlit_style = """
<style>
#MainMenu {visibility: visible;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

pd.options.display.width = 1000
pd.options.display.max_colwidth = 9999

# Load the JSON file
@st.cache_resource()
def load_data(conversations):
    with open(conversations) as f:
        data = json.load(f)
    return data

# @st.cache_resource(suppress_st_warning=True)
# def load_data():
#     conversations = st.sidebar.file_uploader("Load Conversation History File")
#     if conversations is not None:
#         data = json.loads(conversations.read().decode("utf-8"))
#         return data
#     else:
#         return None
# 
@st.cache_resource()
def bytes_to_string(conversations):
    if conversations is not None:
        data = json.loads(conversations.read().decode("utf-8"))
        return data

    return None

def extract_messages(mapping):
    messages = []
    for key, value in mapping.items():
        message_data = value.get("message")
        if message_data:
            if message_data.get("create_time") is not None:
                create_time = datetime.fromtimestamp(message_data.get("create_time")).strftime('%Y-%m-%d %H:%M:%S')
            author = message_data.get("author", {}).get("role")
            content = " ".join(message_data.get("content", {}).get("parts", []))
            messages.append([create_time, author, content])
    return messages


def detect_latex(content):
    # replace \(...\) with $...$
    content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)
    # replace $$...[] with $$...$$
    content = re.sub(r'\$\$(.*?)\[\]', r'$$\1$$', content)
    return content

def main():

    #conversations = st.text_input("Chat History File (JSON):", "conversations.json")
    conversations = st.sidebar.file_uploader("Load Conversation History File")
    data = bytes_to_string(conversations)
#    data = load_data()
    if data is not None:
    #if conversations is not None:
        #file_contents = conversations.read().decode("utf-8")
        
        # Process the JSON data as needed

    #if os.path.isfile(conversations):
    #    data = load_data(conversations)

        # Sidebar
        st.sidebar.title("Conversations")
        selected_conversation = st.sidebar.selectbox(
            "Select a conversation", options=[item["title"] for item in data], index=0
        )

        # Main
        st.title(selected_conversation)

        for conversation in data:
            if conversation["title"] == selected_conversation:
                messages = extract_messages(conversation["mapping"])
#                df = pd.DataFrame(messages, columns=["Timestamp", "Author", "Content"])
#                st.table(df)
                for message in messages:
                    content = detect_latex(message[2])
                    st.markdown(f"**{message[1]} at {message[0]}**: {content}")

if __name__ == "__main__":
    main()
