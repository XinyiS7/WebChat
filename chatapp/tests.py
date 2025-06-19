from django.test import TestCase

# Create your tests here.
import requests
response = requests.post(
  "https://api.deepseek.com/chat/completions",
  headers={
      "Authorization": "Bearer sk-a...",
      "Content-Type": "application/json"
  },
  json={
      "model": 'deepseek-coder',
      "messages": [{"role": "user", "content": "写一个Python快速排序"}]
  }
)
print(response.json())

response = requests.get(
    "https://api.deepseek.com/models",  # 或者尝试 /v1/models
    headers={
        "Authorization": "Bearer sk-a06cc95626404a74bc1d7f310c0751cc",
        "Content-Type": "application/json"
    }
)
print(response.json())