import ollama

model='llama3.2:3b'

print('--- Without example ---')
print(ollama.generate(model, prompt='Will Santa bring me presents on Christmas')['response'])

print('--- Scoring with persona ---')
print(ollama.generate(model, prompt='Q: Is the tooth fairy real? A: Of course! Put your tooth under your pillow tonight. The tooth fairy might visit and leave you something. Q: Will Santa bring me presents on Christmas? A:')['response'])