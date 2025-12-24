import streamlit as st
from plagiarism_checker import check_plagiarism
import PyPDF2
import docx

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
    Now with *file upload support* (TXT, PDF, DOCX)!
    """
)

# ----------------- Input Mode -----------------
mode = st.radio("Choose Input Mode", ["Text Input", "File Upload"])

# ----------------- Text Input -----------------
if mode == "Text Input":
    input_text = st.text_area(
        "Enter the original text:",
        height=200
    )
    reference_text = st.text_area(
        "Enter the reference text:",
        height=200
    )

# ----------------- File Upload -----------------
elif mode == "File Upload":
    uploaded_file = st.file_uploader("Upload a file", type=["txt","pdf","docx"])
    reference_text = st.text_area(
        "Enter reference text for comparison:",
        height=200
    )

# ----------------- File Extraction Function -----------------
def extract_text(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type == "application/pdf":
        pdf = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file.type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                       "application/msword"]:
        doc = docx.Document(file)
        return "\n".join(para.text for para in doc.paragraphs)
    else:
        st.warning("Unsupported file type")
        return ""

# ----------------- Check Plagiarism -----------------
if st.button("Check Plagiarism"):
    # Text Input Mode
    if mode == "Text Input":
        if input_text.strip() == "" or reference_text.strip() == "":
            st.warning("Please enter text in both fields.")
        else:
            score = check_plagiarism(input_text, reference_text)
            st.subheader("Result")
            st.success(f"Plagiarism Similarity Score: {score}%")

            if score > 80:
                st.error("⚠️ High plagiarism detected")
            elif score > 40:
                st.warning("⚠️ Moderate plagiarism detected")
            else:
                st.info("✅ Low plagiarism detected")

    # File Upload Mode
    elif mode == "File Upload":
        if uploaded_file is None:
            st.warning("Please upload a file to check.")
        elif reference_text.strip() == "":
            st.warning("Please enter reference text for comparison.")
        else:
            file_text = extract_text(uploaded_file)
            if file_text.strip() == "":
                st.warning("Uploaded file is empty or could not extract text.")
            else:
                score = check_plagiarism(file_text, reference_text)
                st.subheader("Result")
                st.success(f"Plagiarism Similarity Score: {score}%")

                if score > 80:
                    st.error("⚠️ High plagiarism detected")
                elif score > 40:
                    st.warning("⚠️ Moderate plagiarism detected")
                else:
                    st.info("✅ Low plagiarism detected")