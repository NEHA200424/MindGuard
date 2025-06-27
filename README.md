# MindGuard – AI-Powered Mental Wellness App

MindGuard is an intelligent mental wellness web application that analyzes user input, detects emotions, and responds with personalized, empathetic suggestions. It uses machine learning and conversational AI to simulate a supportive mental health chat experience.

---

## Features

- Detects emotions like joy, sadness, anger, fear, and more
- Provides supportive suggestions based on emotional state
- Smart AI chatbot replies with typing animation
- Chat history stored and retrieved from database
- Dark mode and light mode toggle
- Clean and modern user interface
- Fully deployable frontend and backend

---

## Technologies Used

- HTML, CSS, JavaScript
- Python, Flask, Flask-CORS
- scikit-learn, joblib, pandas
- Hugging Face Datasets (GoEmotions)
- SQLite for storing chat history

---

## Folder Structure

MindGuard/
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── script.js
├── backend/
│ ├── app.py
│ ├── requirements.txt
│ └── model/
│ ├── emotion_model.pkl
│ └── vectorizer.pkl
└── README.md

## How to Run

1. Clone the repository
2. Set up the Python backend
   - Install dependencies from `requirements.txt`
   - Run `app.py` to start the Flask server
3. Open `index.html` in browser to use the frontend
4. Make sure the frontend API calls point to your Flask server URL

---

## About

Created by Neha Vinod Varma  
B.Tech Artificial Intelligence & Machine Learning 
