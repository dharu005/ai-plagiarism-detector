import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Plagiarism Detection System",
    layout="wide"
)

# App Title
st.title("AI-Based Plagiarism Detection System")

# Description
st.write(
    "This application detects plagiarized content using NLP techniques. "
    "Users will be able to input text or upload documents for analysis."
)

# Placeholder sections
st.subheader("Input Section")
st.info("Text input and file upload functionality will be added here.")

st.subheader("Results Section")
st.info("Plagiarism results will be displayed here.")