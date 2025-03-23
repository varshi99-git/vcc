from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = {"reply": f"Watson AI Response to: {user_input}"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)