import streamlit as st
from utils.mcp import mcp_list_tools, mcp_call_tools
from utils.llm import determine_function_call, stream_response
from utils.prompt import amend_prompt_with_tool

# load env variables
API_KEY = st.secrets["API_KEY"]

# initiate session
if "history" not in st.session_state:
    st.session_state["history"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# streamlit layout
st.set_page_config(
    page_title="AI Agent",
    page_icon=":robot:"
)
st.header("AI Agent")
# add button to clear session
if st.button("Clear Session", type = "primary"):
    st.session_state.clear()
    st.rerun()

# get mcp tools from mcp server
tools = mcp_list_tools()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask anything"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display LLM response in chat message container
    with st.chat_message("assistant"):
        # check if any function call is needed from user's prompt
        function_to_call = determine_function_call(tools, prompt)
        if function_to_call:
            result = mcp_call_tools(function_to_call)
            st.write("Identified Tool to call")
            st.code(function_to_call)
            prompt = amend_prompt_with_tool(prompt, result)
        response = st.write_stream(stream_response(prompt))
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
