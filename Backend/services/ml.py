import requests
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_response(message: str) -> str:
    logger.info(f"📨 Запрос к модели: {message}")
    try:
        # phi:latest               e2fd6321a5fe    1.6 GB    
        # gemma:2b                 b50d6c999e59    1.7 GB    
        # qwen:14b                 80362ced6553    8.2 GB    
        # qwen:7b                  2091ee8c8d8f    4.5 GB    
        # deepseek-coder:33b       acec7c0b0fd9    18 GB    
        # mistral:latest           3944fe81ec14    4.1 GB   
        # deepseek-coder:6.7b      ce298d984115    3.8 GB   
        # deepseek-coder:latest    3ddd2d3fc8d2    776 MB   
        # llama3:latest            365c0bd3c000    4.7 GB   
        response = requests.post(
            "http://ollama:11434/api/chat",
            json={
                "model": "llama3:latest",
                "messages": [{"role": "user", "content": message}],
                "stream": True
            },
            timeout=60
        )

        result = ""
        for line in response.iter_lines(decode_unicode=True):
            if line.strip():
                try:
                    data = json.loads(line)
                    content = data.get("message", {}).get("content")
                    if content:
                        result += content
                except json.JSONDecodeError as je:
                    logger.warning(f"⚠️ Ошибка JSON-декодирования: {je}")
                    continue

        if not result.strip():
            logger.warning("⚠️ Пустой ответ от модели")
            return "⚠️ Модель не дала ответ. Попробуйте переформулировать."

        logger.info(f"📤 Ответ модели: {result[:200]}...")  # лог только первые 200 символов
        return result

    except Exception as e:
        logger.error(f"❌ Ошибка запроса к модели: {e}")
        return f"⚠️ Ошибка генерации ответа. Попробуйте позже.\n\n{str(e)}"
