import streamlit as st
from plagiarism_checker import check_plagiarism
import PyPDF2
import docx
import nltk
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')


# Page Configuration
st.set_page_config(
    page_title="AI-Based Plagiarism Detection System",
    layout="wide"
)

# App Title
st.title("AI-Based Plagiarism Detection System")
st.write("Sentence-wise plagiarism detection with highlighted UI")

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
    
# ---------------- SENTENCE-WISE CHECK ----------------
def sentence_plagiarism(sentences, reference):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([reference] + sentences)
    ref_vec = tfidf[0:1]
    sent_vec = tfidf[1:]
    scores = cosine_similarity(sent_vec, ref_vec)
    return scores

# ----------------- Check Plagiarism -----------------
if st.button("Check Plagiarism"):
    if mode == "File Upload":
        if uploaded_file is None:
            st.warning("Upload a file")
            st.stop()
        input_text = extract_text(uploaded_file)

    if input_text.strip() == "" or reference_text.strip() == "":
        st.warning("Please provide both texts")
        st.stop()

    sentences = sent_tokenize(input_text)
    scores = sentence_plagiarism(sentences, reference_text)

    st.subheader("Sentence-wise Analysis (Day 5)")

    for i, sentence in enumerate(sentences):
        percent = round(scores[i][0] * 100, 2)

        if percent > 40:
            st.markdown(
                f"""
                <div style="
                    background-color:#ffe5e5;
                    padding:10px;
                    border-left:6px solid red;
                    border-radius:8px;
                    margin-bottom:10px;">
                    <b>Plagiarized ({percent}%)</b><br>
                    {sentence}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="
                    background-color:#e5ffe5;
                    padding:10px;
                    border-left:6px solid green;
                    border-radius:8px;
                    margin-bottom:10px;">
                    <b>Original ({percent}%)</b><br>
                    {sentence}
                </div>
                """,
                unsafe_allow_html=True
            )