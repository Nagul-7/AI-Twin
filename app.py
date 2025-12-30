# app.py

from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Call your existing AI Twin via subprocess
    result = subprocess.run(
        ["python", "query.py"],
        input=user_input + "\nexit\n",
        text=True,
        capture_output=True
    )

    output = result.stdout.split("🤖 AI Twin:")[-1].strip()
    return jsonify({"reply": output})


if __name__ == "__main__":
    app.run(debug=True)
