import requests
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_response(message: str) -> str:
    logger.info(f"📨 Запрос к модели: {message}")
    
    try:
        response = requests.post(
            "http://ollama:11435/api/chat",
            json={
                "model": "llama3:latest",  # или другую модель, если нужно
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
                    logger.warning(f"⚠️ JSON-декодирование не удалось: {je}")
                    continue

        if not result.strip():
            logger.warning("⚠️ Модель не вернула осмысленный ответ")
            return "⚠️ Модель не дала ответ. Попробуйте переформулировать запрос."

        logger.info(f"📤 Ответ от модели: {result[:200]}...")  # лог первых 200 символов
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка соединения с моделью: {e}")
        return f"⚠️ Ошибка подключения к модели. Убедитесь, что сервис работает.\n\n{str(e)}"
    
    except Exception as e:
        logger.error(f"❌ Неизвестная ошибка генерации ответа: {e}")
        return f"⚠️ Внутренняя ошибка. Попробуйте позже.\n\n{str(e)}"
