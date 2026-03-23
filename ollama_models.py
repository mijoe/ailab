import ollama

response = ollama.list()

print(f"{'Model Name':<30} | {'Size':<10} | {'Quantization'}")
print("-" * 60)

for model in response['models']:
    name = model['model']
    size_gb = f"{model['size'] / 1e9:.2f} GB"
    
    # Quantization is often stored inside details -> quantization_level
    quant = model.get('details', {}).get('quantization_level', 'Unknown')
    
    print(f"{name:<30} | {size_gb:<10} | {quant}")
