from ollama import ChatResponse
from ollama import Client

client = Client(
    host='127.0.0.1:11434',
)

response: ChatResponse = client.chat(model='qwen3.5:9b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
], stream=True)
for part in response:
    print(part['message']['content'], end='', flush=True)