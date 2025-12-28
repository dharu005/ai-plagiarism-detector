import streamlit as st
import pandas as pd
import nltk
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from docx import Document
from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Plagiarism Detection and Correction System",
    layout="wide"
)

# ------------------ DARK GRADIENT THEME ------------------
st.markdown("""
<style>
/* ---------------- APP BACKGROUND ---------------- */
.stApp {
    background: linear-gradient(135deg, #7c3aed, #3b82f6, #ec4899);
    color: #f3f4f6;
    font-family: 'Poppins', sans-serif;
}

/* ---------------- TITLE ---------------- */
h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    color: #ffffff;
    margin-bottom: 25px;
}

/* ---------------- HEADINGS ---------------- */
h2, h3 {
    color: #e0e7ff;
    font-weight: 600;
}

/* ---------------- SENTENCE BOXES ---------------- */
.result-box {
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
    font-size: 15px;
    background: rgba(0,0,0,0.3); /* slightly transparent dark */
    color: #f3f4f6;
    border-left: 6px solid; /* colored left line */
}

.original {
    border-color: #10b981; /* green line */
}

.plagiarized {
    border-color: #ef4444; /* red line */
}

/* ---------------- REWRITTEN CONTENT ---------------- */
.rewrite-box {
    background: rgba(0,0,0,0.3); /* subtle dark background */
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #7c3aed;
    line-height: 1.6;
    color: #000000; /* black text */
}

/* ---------------- INPUTS ---------------- */
textarea, input, .stFileUploader {
    background-color: rgba(0,0,0,0.5) !important;
    color: #f3f4f6 !important;
    border-radius: 10px !important;
    border: 1px solid #7c3aed !important;
}

/* ---------------- BUTTON ---------------- */
button[kind="primary"] {
    background: linear-gradient(90deg, #7c3aed, #3b82f6, #ec4899) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 0.6rem 1.2rem !important;
    transition: 0.3s;
}
button[kind="primary"]:hover {
    opacity: 0.85;
}

/* ---------------- COLUMNS ---------------- */
.stColumn > div {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

/* ---------------- FOOTER ---------------- */
.footer {
    text-align: center;
    color: #f3f4f6;
    margin-top: 40px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ FONT STYLE ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lobster&family=Montserrat:wght@400;600;700;900&display=swap');

/* Title */
h1 {
    font-family: 'Lobster', cursive;
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    color: #ffffff; /* filled text for clarity */
    background: linear-gradient(90deg, #7c3aed, #3b82f6, #ec4899);
    padding: 15px 30px;
    border-radius: 15px;
    display: inline-block;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.4);
    margin-bottom: 40px;
}

/* Headings */
h2, h3, label {
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    color: #f3f4f6;
}

/* Inputs, radio buttons, select boxes, file uploader labels */
.stRadio label, .stSelectbox label, .stTextArea label, .stFileUploader label {
    font-family: 'Montserrat', sans-serif;
    font-weight: 600;
    color: #f3f4f6;
}
</style>
""", unsafe_allow_html=True)


# ------------------ TITLE ------------------
st.markdown("""
<h1 style="
    font-family: 'Cursive', 'Poppins', sans-serif;
    font-size: 4rem;
    font-weight: 900;
    text-align: center;
    color: #ffffff; /* white fill for clarity */
    background: linear-gradient(90deg, #7c3aed, #3b82f6, #ec4899);
    -webkit-background-clip: padding-box; /* normal fill */
    padding: 15px 20px;
    border-radius: 15px;
    display: inline-block;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.4);
    margin-bottom: 40px;
">
 Plagiarism Detection and Correction System 
</h1>
""", unsafe_allow_html=True)

# ------------------ NLTK SETUP ------------------
@st.cache_resource
def setup_nltk():
    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")
    nltk.download("wordnet")
    nltk.download("omw-1.4")
setup_nltk()

# ------------------ LOAD DATASET ------------------
@st.cache_data
def load_dataset():
    df = pd.read_csv("plagiarism_dataset.csv")
    return df.iloc[:, 0].astype(str).tolist()
REFERENCE_TEXTS = load_dataset()

# ------------------ FILE EXTRACTION ------------------
def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return " ".join(p.extract_text() or "" for p in reader.pages)
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return " ".join(p.text for p in doc.paragraphs)
    return ""

# ------------------ PLAGIARISM DETECTION ------------------
def detect_plagiarism(sentences, references, threshold=0.30):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(references + sentences)
    ref_vec = tfidf[:len(references)]
    sent_vec = tfidf[len(references):]
    similarity_matrix = cosine_similarity(sent_vec, ref_vec)
    results = []
    for i, sent in enumerate(sentences):
        score = similarity_matrix[i].max()
        results.append((sent, score, score >= threshold))
    return results

# ------------------ WEB REFERENCES ------------------
def web_references(text):
    query = " ".join(text.split()[:10])
    refs = []
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    for r in results:
        try:
            page = requests.get(r["href"], timeout=5)
            soup = BeautifulSoup(page.text, "html.parser")
            content = " ".join(p.get_text() for p in soup.find_all("p"))
            if content.strip():
                refs.append(content)
        except:
            pass
    return refs

# ------------------ WORDNET REWRITE ------------------
def get_wordnet_pos(tag):
    if tag.startswith("J"): return wordnet.ADJ
    if tag.startswith("V"): return wordnet.VERB
    if tag.startswith("N"): return wordnet.NOUN
    if tag.startswith("R"): return wordnet.ADV
    return None

def rewrite_sentence(sentence):
    words = word_tokenize(sentence)
    tagged = pos_tag(words)
    rewritten = []
    for word, tag in tagged:
        wn_pos = get_wordnet_pos(tag)
        if wn_pos:
            synsets = wordnet.synsets(word, pos=wn_pos)
            rewritten.append(
                synsets[0].lemmas()[0].name().replace("_", " ") if synsets else word
            )
        else:
            rewritten.append(word)
    return " ".join(rewritten)[:1].upper() + " ".join(rewritten)[1:]

# ------------------ UI ------------------
st.markdown("##  Configuration")
col1, col2 = st.columns([1, 3])

with col1:
    mode = st.radio(
        "Mode",
        ["Text Input", "File Input", "Compare Two Texts", "Compare Two Files"]
    )
    source = st.selectbox(
        "Detection Source",
        ["Hybrid", "Dataset", "Web"]
    )

with col2:
    text1 = text2 = ""
    if mode == "Text Input":
        text1 = st.text_area("Enter text", height=180)
    elif mode == "File Input":
        file = st.file_uploader("Upload file", ["pdf", "docx", "txt"])
        if file: text1 = extract_text(file)
    elif mode == "Compare Two Texts":
        text1 = st.text_area("Text 1", height=120)
        text2 = st.text_area("Text 2", height=120)
    elif mode == "Compare Two Files":
        f1 = st.file_uploader("File 1", ["pdf", "docx", "txt"], key="1")
        f2 = st.file_uploader("File 2", ["pdf", "docx", "txt"], key="2")
        if f1 and f2:
            text1 = extract_text(f1)
            text2 = extract_text(f2)

# ------------------ CHECK BUTTON ------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button(" 🚀Check Plagiarism", use_container_width=True):
    if not text1.strip():
        st.warning("Please provide input text")
        st.stop()

    final_output = []
    if mode in ["Compare Two Texts", "Compare Two Files"]:
        s1 = sent_tokenize(text1)
        s2 = sent_tokenize(text2)
        results = detect_plagiarism(s1, s2)
    else:
        sentences = sent_tokenize(text1)
        references = REFERENCE_TEXTS.copy()
        if source != "Dataset Only":
            references += web_references(text1)
        results = detect_plagiarism(sentences, references)

    st.markdown("##  Sentence-wise Analysis")
    for sent, score, plag in results:
        percent = int(score * 100)
        if plag:
            rewritten = rewrite_sentence(sent)
            final_output.append(rewritten)
            st.markdown(
                f"<div class='result-box plagiarized'><b>Plagiarized ({percent}%)</b><br>{sent}</div>",
                unsafe_allow_html=True
            )
        else:
            final_output.append(sent)
            st.markdown(
                f"<div class='result-box original'><b>Original ({percent}%)</b><br>{sent}</div>",
                unsafe_allow_html=True
            )

    st.markdown("##  Rewritten Content")
    st.markdown(
        f"<div class='rewrite-box'>{' '.join(final_output)}</div>",
        unsafe_allow_html=True
    )

# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer">
AI Plagiarism Detection System • TF-IDF • Cosine Similarity • WordNet • Dataset + Web
</div>
""", unsafe_allow_html=True)
