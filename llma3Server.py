import requests
from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os



load_dotenv()
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    raise ValueError("Hugging Face API key가 .env 파일에 설정되어 있지 않습니다.")
# Hugging Face Inference API 설정
client = InferenceClient(api_key=api_key)

# Hugging Face Inference API 설정
API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
headers = {"Authorization": f"Bearer {api_key}"}

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running"

@app.route("/review", methods = ["POST"])
def review():
    data = request.json
    code_diff = data.get("code_diff", "")
    code_context = data.get("code_context", "")

    # 리뷰 프롬프트
    prompt = (
        "Please review the following code changes with a focus on the criteria below:\n\n"
        "1. **Pre-condition Check**:\n"
        "   Verify that the function or method is correctly set up to operate as expected. "
        "Ensure that variables have valid states or fall within the required ranges.\n\n"
        "2. **Runtime Error Check**:\n"
        "   Inspect the code for any potential runtime errors or hidden risks. "
        "Highlight areas that may cause unexpected failures during execution.\n\n"
        "3. **Optimization**:\n"
        "   Analyze the code for optimization opportunities. If the code is likely to cause performance degradation, "
        "suggest optimized solutions or improvements.\n\n"
        "4. **Security Issue**:\n"
        "   Check for severe security vulnerabilities. Ensure that the code does not use insecure modules "
        "or contain exploitable weaknesses.\n\n"
        "After generating the review, please translate the entire result into Korean for better understanding.\n\n"
        f"Here is the code diff for review:\n\n{code_diff}"
    )

    # messages = [{"role": "user", "content": prompt}]
    #
    # completion = client.chat.completions.create(
    #     model="meta-llama/Llama-3.3-70B-Instruct",
    #     messages=messages,
    #     max_tokens=1000  # 한글 번역을 포함하므로 max_tokens를 늘림
    # )
    #
    # review_comment = completion.choices[0].message["content"]
    # return jsonify({"review": review_comment})

    # Hugging Face Inference API 호출
    try:
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # HTTP 에러 발생 시 예외를 던짐
        result = response.json()
        review_comment = result.get("generated_text", "No review generated.")
    except Exception as e:
        review_comment = f"Error generating review: {e}"

    return jsonify({"review": review_comment})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8680)