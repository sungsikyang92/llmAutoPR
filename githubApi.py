import requests

def fetch_pr_files(repo_name, pr_number, token):
    """
    GitHub API를 통해 PR의 변경된 파일 정보를 가져옵니다.
    """
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 상태 코드 확인
        files = response.json()
        diffs = [file["patch"] for file in files if "patch" in file]
        return diffs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PR files: {e}")
        return []

def post_pr_comment(repo_name, pr_number, token, comment):
    """
    Github PR에 댓글을 추가합니다.
    """
    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"body": comment}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # HTTP 상태 코드 확인
        print("Review comment posted successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error posting comment: {e}")