import ollama

print('--- Temperature 0.0 ---')
print(ollama.generate(model='llama3.2:3b', prompt='What is the name of the highest building in the world?',
      options=dict(temperature=0.0))['response'])

print('--- Temperature 0.7 ---')
print(ollama.generate(model='llama3.2:3b', prompt='What is the name of the highest building in the world?',
      options=dict(temperature=0.7))['response'])

print('--- Temperature 1.2 ---')
print(ollama.generate(model='llama3.2:3b', prompt='What is the name of the highest building in the world?',
      options=dict(temperature=1.2))['response'])
