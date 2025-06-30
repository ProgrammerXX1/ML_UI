import requests

# Адрес API
BASE_URL = "http://localhost:8080"

# Логин — получение JWT токена
def login(username: str, password: str):
    response = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
    response.raise_for_status()
    return response.json()['access_token']

# Запрос к защищённому эндпоинту с JWT
def access_protected(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/jwt-protected", headers=headers)
    response.raise_for_status()
    return response.json()

# Запрос с API ключом
def access_with_api_key(api_key: str):
    headers = {"X-API-Key": api_key}
    response = requests.get(f"{BASE_URL}/api-key-protected", headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    token = login("your_username", "your_password")
    print("JWT Access:", access_protected(token))

    api_key = "your_api_key_here"
    print("API Key Access:", access_with_api_key(api_key))
