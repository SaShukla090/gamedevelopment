import streamlit as st
import requests
import base64
import os
from groq import Client
api = os.getenv("GROQ_API_KEY")
# Initialize the Groq client using the API key from environment variables
client = Client(api_key=api)
 
# Define the function to query Groq's LLM
def query_groq_llm(prompt, model="llama3-8b-8192"):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    return chat_completion.choices[0].message.content
 
# Streamlit app interface
st.title("LLM-powered Game Developer Assistant")
 
# Model selection
models = ["llama3-8b-8192", "groq-llm-2", "groq-llm-3"]  # Example model IDs, adjust as needed
model_id = st.selectbox("Choose a Groq LLM model:", models)
 
# Text input for prompts
prompt = st.text_area("Enter your prompt:")
 
# File upload section
uploaded_files = st.file_uploader("Upload your game files (.js, .html, .css):", accept_multiple_files=True)
 
# Display file content
if uploaded_files:
    for uploaded_file in uploaded_files:
        st.write(f"### {uploaded_file.name}")
        content = uploaded_file.read().decode("utf-8")
        st.code(content, language=uploaded_file.type.split('/')[-1])
 
# Submit button
if st.button("Submit to LLM"):
    full_prompt = prompt
    for uploaded_file in uploaded_files:
        content = uploaded_file.read().decode("utf-8")
        full_prompt += f"\n\n{uploaded_file.name}:\n{content}"
 
    # Query Groq LLM
    response = query_groq_llm(full_prompt, model_id)
    st.write("### LLM Response:")
    st.write(response)
 
    # Option to generate downloadable files
    st.write("### Downloadable Files")
    for file_type in ["html", "css", "js"]:
        if st.button(f"Generate {file_type.upper()} File"):
            file_content = f"// Generated {file_type.upper()} file\n" + response
            b64 = base64.b64encode(file_content.encode()).decode()
            href = f'<a href="data:file/{file_type};base64,{b64}" download="generated.{file_type}">Download generated.{file_type}</a>'
            st.markdown(href, unsafe_allow_html=True)
