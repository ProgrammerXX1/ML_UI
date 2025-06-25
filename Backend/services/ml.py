import requests
import json

def generate_response(message: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",
                "messages": [{"role": "user", "content": message}],
                "stream": True  # оставляем стрим
            },
            stream=True,
            timeout=60
        )

        result = ""
        for line in response.iter_lines(decode_unicode=True):
            if line.strip():
                data = json.loads(line)
                content = data.get("message", {}).get("content")
                if content:
                    result += content
        return result or "[Empty response]"

    except Exception as e:
        return f"Error from model: {str(e)}"
