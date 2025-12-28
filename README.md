# ai-plagiarism-detector
🤖An **AI-based plagiarism detection and rewriting system** that analyzes textual content at the **sentence level** using **Natural Language Processing (NLP)** techniques.

## ⚡ Project Overview
This project detects plagiarism in text documents by comparing user input against reference sources using **TF-IDF vectorization** and **cosine similarity**.  
Plagiarized sentences are identified and automatically rewritten using **WordNet-based synonym replacement** to improve originality.

## 📚 Problem Statement
- Plagiarism is a major concern in academics and content creation. Manual detection is time-consuming and unreliable. 
- This project automates plagiarism detection using machine learning and NLP techniques.
- Identify plagiarized sentences and generate rewritten alternatives.

## 🎯 Objectives
- Detect plagiarized content in text documents📄
- Support multiple input formats🗂️ (TXT, PDF, DOCX)
- Provide sentence-wise plagiarism analysis🟢🔴
- Automatically rewrite plagiarized sentences
- Provide an interactive application for plagiarism analysis💻

## 🛠️ Technologies Used
- Python 3.9+
- Streamlit
- Natural Language Toolkit (NLTK)
- Scikit-learn
- Pandas

## 🧠 How It Works

1. User input is collected as text or uploaded file
2. Text is split into individual sentences
3. TF-IDF vectors are generated for comparison
4. Cosine similarity is calculated against reference data
5. Sentences above the similarity threshold are marked plagiarized
6. Plagiarized sentences are rewritten using WordNet synonyms
7. Final rewritten output is generated

## 📊 7-Day Project Plan

| Day | Work Completed |
|----|---------------|
| Day 1 | Project setup, GitHub repository, basic plagiarism check |
| Day 2 | Text preprocessing and similarity score interpretation |
| Day 3 | File upload support (TXT, PDF, DOCX) |
| Day 4 | Sentence-wise plagiarism detection |
| Day 5 | Classification of original vs plagiarized sentences |
| Day 6 | Rewriting plagiarized sentences using WordNet |
| Day 7 | Final integration, comparison modes, documentation |

## 🚀 How to Run the Project

1️⃣ Install Dependencies

   pip install -r requirements.txt

2️⃣Run the Application

   Run Streamlit app:
   ```bash
   streamlit run app.py