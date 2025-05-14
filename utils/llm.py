import streamlit as st
from google.genai import types
from google import genai

API_KEY = st.secrets["API_KEY"]


def determine_function_call(tools, prompt):
    print("Determining function to call ...")
    # initiatise llm client
    genai_client = genai.Client(api_key = API_KEY)
    response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                tools=tools,
            ))

    # Check for a function call
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Identified function to call: {function_call.name} with args: {function_call.args}")
        return {"name": function_call.name, "arguments": function_call.args}
    else:
        print("No function to call")
        return None

def stream_response(prompt):
    client = genai.Client(api_key = API_KEY)
    response = client.models.generate_content_stream(
    model="gemini-2.0-flash",
    contents=[prompt]
    )
    for chunk in response:
        yield chunk.text