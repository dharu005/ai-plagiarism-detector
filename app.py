import streamlit as st
from plagiarism_checker import check_plagiarism
import PyPDF2
import docx
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from nltk.corpus import wordnet
nltk.download('punkt')
nltk.download('wordnet')

# ------------------ Page Configuration ------------------

st.set_page_config(
    page_title="Plagiarism Detection and correction System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ Stylish Gradient Title ------------------
st.markdown("""
    <h1 style='text-align: center; background: linear-gradient(to right, #30CFD0 0%, #330867 100%);
                -webkit-background-clip: text; color: transparent; font-family: "Segoe UI", sans-serif;'>
        Plagiarism Detection and Correction System
    </h1>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; font-size:16px; color:gray;'>Sentence-wise plagiarism detection with highlights</p>", unsafe_allow_html=True)

# ----------------- Input Mode -----------------
mode = st.radio("Choose Input Mode", ["Text Input", "File Upload"])
input_text = ""
reference_text = ""

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

# ----------------- Simple Rewriting Function -----------------
def rewrite_sentence(sentence):
    words = word_tokenize(sentence)
    new_words = []
    for word in words:
        synonyms = wordnet.synsets(word)
        if synonyms:
            # Take the first lemma as a simple replacement
            new_word = synonyms[0].lemmas()[0].name().replace("_", " ")
            if new_word.lower() != word.lower():
                new_words.append(new_word)
            else:
                new_words.append(word)
        else:
            new_words.append(word)
    return " ".join(new_words)


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

    st.subheader("Sentence-wise Analysis ")
    report_data = []
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

    # ---------------- Download Report ----------------
    report_df = pd.DataFrame(report_data)
    csv = report_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Sentence-wise Report as CSV",
        data=csv,
        file_name="plagiarism_report.csv",
        mime="text/csv"
    )