import requests
from typing import List, Dict, Union

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

class ChatResponse:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

class GearMindError(Exception):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class GearMindSDK:
    def __init__(self, api_key: str, base_url: str = "https://gearmind.geworn.cloud/api/v1"):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, messages: List[Message]) -> ChatResponse:
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                headers=self.headers,
                json={"messages": [{"role": msg.role, "content": msg.content} for msg in messages]}
            )

            response.raise_for_status()
            data = response.json()
            return ChatResponse(role=data["role"], content=data["content"])

        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                try:
                    error_data = e.response.json()
                    error_message = error_data.get("error", f"HTTP error! status: {e.response.status_code}")
                except ValueError:
                    error_message = f"HTTP error! status: {e.response.status_code}"
                raise GearMindError(error_message, e.response.status_code)
            elif isinstance(e, requests.exceptions.ConnectionError):
                raise GearMindError("Failed to make request to GearMind API")
            else:
                raise GearMindError("Unknown error occurred")