import ollama

model='llama3.2:3b'

print('--- Output without format ---')
print(ollama.generate(model, prompt='Answer with Yes or No. "Will Santa bring me presents on Christmas?"')['response'])

print('--- Output without format ---')
print(ollama.generate(model, prompt='Answer with Yes or No. In JSON format. "Will Santa bring me presents on Christmas?"')['response'])

print('--- Output without bool format ---')
print(ollama.generate(model, prompt='Answer with Yes or No. In JSON format with field "presents" as bool. "Will Santa bring me presents on Christmas?"')['response'])

