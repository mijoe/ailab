import ollama

# Models referenced in the code base (keep in sync with ENVIRONMENT.md -> "Required Ollama Models")
required_models = [
    "llama3.2:3b",          # temperature_experiment.py, validate_environment.py, prompt_engineering/*, rag/rag_integration.py
    "ministral-3:8b",       # test_ollama.py, validate_environment.py (hint), prompt_engineering/adopt_persona.py, chain_of_thought_corruption.py
    "ministral-3:14b",      # prompt_engineering/adversarial.py, chain_of_thought.py, chain_of_thought_corruption.py (audit)
    "llama-guard3:8b",      # prompt_engineering/chain_of_thought_corruption.py (audit)
    "qwen2.5:14b",          # prompt_engineering/chain_of_thought_corruption.py (audit)
    "mxbai-embed-large:latest",  # rag/rag_ingest.py, rag_integration.py, similarity_search.py, chunking_strategies_testing.py
]

failed = []
for model_name in required_models:
    print(f"Starting pull for {model_name}...")
    try:
        # This will download the model (no-op for layers already present).
        # stream=True yields progress updates
        for progress in ollama.pull(model_name, stream=True):
            status = progress.get('status')
            if status:
                print(f"Status: {status}".ljust(60), end='\r')
        print(f"\nSuccessfully pulled {model_name}!")
    except Exception as e:
        print(f"\nFailed to pull {model_name}: {e}")
        failed.append(model_name)

if failed:
    print(f"\n{len(failed)} model(s) failed: {', '.join(failed)}")
    raise SystemExit(1)
print(f"\nAll {len(required_models)} models available.")
