from flask import Flask, request, jsonify
from githubApi import fetch_pr_files, post_pr_comment
from llama3Integration import send_to_llama3
from dotenv import load_dotenv
import os


app = Flask(__name__)

# 기본 상태 확인용 엔드포인트
@app.route("/")
def home():
    return "Flask server is running!"

# GitHub Webhook 처리 엔드포인트
@app.route("/webhook", methods=["POST"])
def handle_webhook():
    payload = request.json # Webhook 이벤트 데이터를 JSON 형식으로 수신
    if not payload:
        return jsonify({"message": "No payload received"}), 400

    # 수신된 데이터 출력
    print(f"Received Webhook payload: {payload}")

    if "pull_request" in payload and payload["action"] in ["opened", "synchronize", "edited", "reopened"]:
        pr_data = payload["pull_request"]
        pr_number = pr_data["number"]
        repo_name = payload["repository"]["full_name"]

        # 로그 출력 (테스트용)
        print(f"PR #{pr_number} opend in repository {repo_name}")
        token = os.getenv("GITHUB_TOKEN")
        diffs = fetch_pr_files(repo_name, pr_number, token)

        for diff in diffs:
            review_comment = send_to_llama3(diff)
            print(f"Llama 3 Review for PR #{pr_number}: {review_comment}")

        return jsonify({"message": f"PR #{pr_number} received and processed."}), 200

    return jsonify({"message": "Not a PR opened event."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8670)