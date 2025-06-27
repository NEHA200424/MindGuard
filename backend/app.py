from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sqlite3
import datetime
import requests

# 🔐 Load environment variables from .env
load_dotenv()

# ✅ App configuration
app = Flask(__name__)
CORS(app)

# 🔑 Secure API Key and Model
API_KEY = os.environ.get("API_KEY")
MODEL = os.environ.get("MODEL", "mistralai/mixtral-8x7b-instruct")

# 🧠 SQLite DB setup
DB_FILE = "chat_history.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                user TEXT,
                bot TEXT
            )
        """)
init_db()

# 🚀 Emotion & Chat Response Endpoint
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    user_input = data.get("text", "").strip()

    if not user_input:
        return jsonify({"error": "No input provided."}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are MindGuard, an AI mental wellness companion. Reply with empathetic, thoughtful, and supportive responses in paragraph format."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        # Save chat to DB
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(
                "INSERT INTO chats (timestamp, user, bot) VALUES (?, ?, ?)",
                (datetime.datetime.now().isoformat(), user_input, reply)
            )

        return jsonify({"reply": reply})

    except Exception as e:
        print("API Error:", e)
        return jsonify({"error": "Failed to get AI response."}), 500

# 🧾 Chat History Endpoint
@app.route("/history", methods=["GET"])
def history():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute(
            "SELECT timestamp, user, bot FROM chats ORDER BY id DESC LIMIT 20"
        ).fetchall()
        return jsonify([
            {"timestamp": row[0], "user": row[1], "bot": row[2]} for row in rows
        ])

# ▶️ Run the app
if __name__ == "__main__":
    app.run(debug=True)
