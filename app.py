import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-04-17:generateContent"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    if not prompt:
        return jsonify(error="No prompt"), 400

    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    body = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        # Optional: You can adjust the "thinking" level
        # "thinkingBudget": 0
    }

    resp = requests.post(GEMINI_URL, headers=headers, params=params, json=body)
    if not resp.ok:
        return jsonify(error=resp.text), resp.status_code

    try:
        data = resp.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify(reply=reply)
    except Exception as e:
        return jsonify(error="Failed to parse response", details=str(e)), 500
