# ai-plagiarism-detector
AI-based Plagiarism detection and rewritting

## Project Overview
This project aims to detect plagiarism in text documents using Natural Language Processing (NLP) techniques. 
The system compares user input against a reference corpus and identifies plagiarized content based on similarity scores.
Supports both *text input* and *file uploads* (TXT, PDF, DOCX). 

## Problem Statement
Plagiarism is a major concern in academics and content creation. Manual detection is time-consuming and unreliable. 
This project automates plagiarism detection using machine learning and NLP techniques.

## Objectives
- Detect plagiarized content in text
- Support multiple input formats
- Provide sentence-wise plagiarism analysis
- Develop a simple web-based interface

## Technologies Used
- Python 3.9+
- Streamlit
- NLTK
- Scikit-learn
- Pandas

## How to Use
   Run Streamlit app:
   ```bash
   streamlit run app.py

## Day

Day 1
Project setup, GitHub repo, basic text input plagiarism check.
Day 2
Text preprocessing, plagiarism score interpretation (low/moderate/high).
Day 3
File upload support (TXT, PDF, DOCX), extract text from files.
Day 4
Sentence-wise plagiarism detection (splitting text into sentences).
Day 5
Highlight plagiarized vs original sentences in the UI.
Day 6
Rewriting plagiarized sentences using WordNet synonyms.
Day 7
UI improvements, two-text/file comparison, optional download of report.