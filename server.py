from flask import Flask, request, jsonify

app = Flask(__name__)

# 기본 상태 확인용 엔드포인트
@app.route("/")
def home():
    return "Flask server is running!"