# Test 1: Verify Ollama connectivity
import ollama
client = ollama.Client(host='http://localhost:11434')
print(client.list())

# Test 2: Simple inference
response = ollama.chat(
    model='ministral-3:latest',
    messages=[{'role': 'user', 'content': 'Say "Connected"'}]
)
print(response['message']['content'])
