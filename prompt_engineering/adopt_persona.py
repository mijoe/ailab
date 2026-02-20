import ollama

model='llama3.2:3b'

print('--- Scoring without persona ---')
print(ollama.generate(model, prompt='Give the essay below a score from 1 to 5, with 1 being very bad and 5 being very good. Be concise. Output only the score and nothing else. "I like chickens. Chickens are fluffy and they give tasty eggs.')['response'])

print('--- Scoring with persona ---')
print(ollama.generate(model, prompt='You are a first-grade teacher. Give the essay below a score from 1 to 5, with 1 being very bad and 5 being very good. Be concise. Output only the score and nothing else. "I like chickens. Chickens are fluffy and they give tasty eggs.')['response'])

print('--- Scoring with german persona ---')
print(ollama.generate(model, prompt='You are a first-grade teacher in Germany. Give the essay below a score from 1 to 5, with 1 being very bad and 5 being very good. Be concise. Output only the score and nothing else. "I like chickens. Chickens are fluffy and they give tasty eggs.')['response'])

print('--- Scoring with pre-school persona ---')
print(ollama.generate(model, prompt='You are a pre-school teacher. Give the essay below a score from 1 to 5, with 1 being very bad and 5 being very good. Be concise. Output only the score and nothing else. "I like chickens. Chickens are fluffy and they give tasty eggs.')['response'])