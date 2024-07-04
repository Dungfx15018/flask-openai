from flask import Flask, request, jsonify
from openai_client import OpenAIClient
from flask_cors import CORS

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAIClient(api_key)

app = Flask(__name__)

CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get('messages', [])

    if not messages:
        return jsonify({"error": "No messages provided"}), 400

    response = openai_client.chat(messages)
    return jsonify({
        "content": response,
        "role": "assistant"
        })

if __name__ == '__main__':
    app.run(debug=True)