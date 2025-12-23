import streamlit as st
from plagiarism_checker import check_plagiarism

# Page Configuration
st.set_page_config(
    page_title="AI-Based Plagiarism Detection System",
    layout="wide"
)

# App Title
st.title("AI-Based Plagiarism Detection System")

# Description
st.write(
    """
    This application detects plagiarism between two texts using
    Natural Language Processing (NLP) techniques.
    """
)

# Input Section
st.header("Input Texts")

input_text = st.text_area(
    "Enter the original text:",
    height=200
)

reference_text = st.text_area(
    "Enter the reference text:",
    height=200
)

# Button
if st.button("Check Plagiarism"):
    if input_text.strip() == "" or reference_text.strip() == "":
        st.warning("Please enter text in both fields.")
    else:
        score = check_plagiarism(input_text, reference_text)

        st.subheader("Result")
        st.success(f"Plagiarism Similarity Score: {score}%")

        # Interpretation
        if score > 80:
            st.error("⚠️ High plagiarism detected")
        elif score > 40:
            st.warning("⚠️ Moderate plagiarism detected")
        else:
            st.info("✅ Low plagiarism detected")