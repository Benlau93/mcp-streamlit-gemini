import streamlit as st
from google.genai import types
import httpx
import json

def extract_json_from_event(raw_event: str):
    for line in raw_event.splitlines():
        if line.startswith("data: "):
            json_str = line[len("data: "):]
            return json.loads(json_str)
    raise ValueError("No data line with JSON found.")

url = st.secrets["MCP_URL"]
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

@st.cache_resource(ttl=600)
def mcp_list_tools():
    # JSON-RPC request format
    payload = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/list",
    }

   # request to mcp server to list all tools available
    response = httpx.post(url, headers=headers, json=payload)
    data =  extract_json_from_event(response.text)
    mcp_tools = data["result"]

    # convert tools retreived into format usable by google gemini
    tools = [
        types.Tool(
            function_declarations=[
                {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": {
                        k: v
                        for k, v in tool["inputSchema"].items()
                        if k not in ["additionalProperties", "$schema"]
                    },
                }
            ]
        )
        for tool in mcp_tools["tools"]
    ]
    return tools

def mcp_call_tools(params):
    call_payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "tools/call",
                "params": params
            }
    response = httpx.post(url, headers=headers, json=call_payload)
    result =  extract_json_from_event(response.text)["result"]["content"][0]["text"]

    return result