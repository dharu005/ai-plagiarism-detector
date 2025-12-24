from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# ----------------- Preprocess Text -----------------
def preprocess_text(text):
    """
    Converts text to lowercase, removes punctuation and stopwords.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    words = text.split()
    filtered = [w for w in words if w not in stop_words]
    return " ".join(filtered)

# ----------------- Check Plagiarism -----------------
def check_plagiarism(text1, text2):
    """
    Returns the plagiarism similarity score (%) between two texts.
    """
    text1 = preprocess_text(text1)
    text2 = preprocess_text(text2)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(score[0][0]*100, 2)