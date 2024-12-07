import requests
import os

def send_to_llama3(diff):
    """
    Llama 3 서버에 코드 diff를 전달하여 리뷰 결과를 반환합니다.
    """
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError("Hugging Face API key가 설정되어 있지 않습니다.")

    # url = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
    url = "http://localhost:8680/review"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": diff}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # 응답 데이터 디버깅
        print(f"API Response: {result}")

        # 응답이 리스트인지, 딕셔너리인지 확인하고 처리
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "No review generated.")
        elif isinstance(result, dict):
            return result.get("generated_text", "No review generated.")
        else:
            return "Unexpected response format from API."

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return f"Error connecting to Llama 3 server: {e}"
