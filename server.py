from flask import Flask, request, jsonify

app = Flask(__name__)

# 기본 상태 확인용 엔드포인트
@app.route("/")
def home():
    return "Flask server is running!"

# GitHub Webhook 처리 엔드포인트
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    payload = request.json # Webhook 이벤트 데이터를 JSON 형식으로 수신
    if "pull_request" in payload and payload["action"] == "opened":
        pr_data = payload["pull_request"]
        pr_number = pr_data["number"]
        repo_name = payload["repository"]["full_name"]

        # 로그 출력 (테스트용)
        print(f"PR #{pr_number} opend in repository {repo_name}")

        # 나중에 Llama 3 모델과 연결
        return jsonify({"message": f"PR #{pr_number} received and processed."}), 200

    return jsonify({"message": "Not a PR opened event."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8670)