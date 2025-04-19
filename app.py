import os
from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL     = "https://gemini.googleapis.com/v1/models/text-bison-001:generateText"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify(error="No prompt provided"), 400

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "prompt": {"text": prompt},
        "temperature": 0.7
    }
    resp = requests.post(GEMINI_URL, headers=headers, json=body)
    if not resp.ok:
        return jsonify(error=resp.text), resp.status_code

    result = resp.json()
    text = result.get("candidates", [{}])[0].get("output", "")
    return jsonify(reply=text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)