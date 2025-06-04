from ollama import chat # type: ignore
from ollama import ChatResponse # type: ignore

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue? keep the response under 10 words',
  },
])
print(response['message']['content'])
print(response.message.content)