import requests
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_response(message: str) -> str:
    logger.info(f"📨 Запрос к модели: {message}")
    
    try:
        response = requests.post(
            "http://10.121.252.227:11434/api/chat",
            json={
                "model": "llama3:latest",  # или твоя конкретная модель
                "messages": [{"role": "user", "content": message}],
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            logger.warning(f"⚠️ Неверный ответ от сервера: {response.status_code}, {response.text}")
            return "⚠️ Ошибка генерации ответа от модели."

        data = response.json()
        content = data.get("message", {}).get("content", "")

        if not content.strip():
            logger.warning("⚠️ Модель не вернула осмысленный ответ")
            return "⚠️ Модель не дала ответ. Попробуйте переформулировать запрос."

        logger.info(f"📤 Ответ от модели: {content[:200]}...")
        return content

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка соединения с моделью: {e}")
        return f"⚠️ Ошибка подключения к модели. Убедитесь, что сервис работает.\n\n{str(e)}"

    except Exception as e:
        logger.error(f"❌ Неизвестная ошибка генерации ответа: {e}")
        return f"⚠️ Внутренняя ошибка. Попробуйте позже.\n\n{str(e)}"