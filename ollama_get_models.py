import ollama

model_name = "qwen3:32b-q4_K_M"

print(f"Starting pull for {model_name}...")

# This will download the model. 
# set stream=True to see progress updates
current_digest = None
for progress in ollama.pull(model_name, stream=True):
    status = progress.get('status')
    
    # Optional: Logic to show percentage or just status updates
    if status:
        print(f"Status: {status}", end='\r')

print(f"\nSuccessfully pulled {model_name}!")