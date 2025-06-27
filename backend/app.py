from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime
import requests

app = Flask(__name__)
CORS(app)

# ✅ Your actual OpenRouter API key
API_KEY = "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"
MODEL = "mistralai/mixtral-8x7b-instruct"  # You can change to "anthropic/claude-3-haiku"

# ✅ Setup SQLite database
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

# ✅ POST endpoint to analyze emotion using Mixtral/Claude
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    user_input = data.get("text", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are MindGuard, an AI mental health companion. Speak in kind, encouraging, detailed paragraphs to help users feel heard and supported."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        reply = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO chats (timestamp, user, bot) VALUES (?, ?, ?)",
                     (datetime.datetime.now().isoformat(), user_input, reply))

    return jsonify({"reply": reply})

# ✅ GET endpoint to fetch chat history
@app.route("/history", methods=["GET"])
def history():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("SELECT timestamp, user, bot FROM chats ORDER BY id DESC LIMIT 20").fetchall()
        return jsonify([
            {"timestamp": row[0], "user": row[1], "bot": row[2]} for row in rows
        ])

if __name__ == "__main__":
    app.run(debug=True)
