import ollama

ollama.generate(model='llama3.2:3b', prompt='What is the name of the highest building in the world?', options=dict(temperature=0.0))['response']

ollama.generate(model='llama3.2:3b', prompt='What is the name of the highest building in the world?', options=dict(temperature=0.7))['response']

ollama.generate(model='llama3.2:3b', prompt='What is the name of the highest building in the world?', options=dict(temperature=1.2))['response']
