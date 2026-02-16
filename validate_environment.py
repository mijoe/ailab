#!/usr/bin/env python3
"""
Environment validation script for AI Engineering Lab
Tests all critical components and configurations
"""

import sys
import os
from pathlib import Path


def test_imports():
    """Verify all required packages are installed"""
    print("🧪 Testing imports...")
    required_packages = [
        "ollama",
        "langchain",
        "langchain_community",
        "openai",
        "dotenv",
        "httpx",
        "pydantic",
        "jupyter",
        "pytest",
        "ruff"
    ]

    failed = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package}: {e}")
            failed.append(package)

    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        return False
    print("✅ All packages imported successfully\n")
    return True


def test_ollama_connection():
    """Verify Ollama is accessible and has models"""
    print("🧪 Testing Ollama connection...")
    import ollama

    try:
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        print(f"  Connecting to: {ollama_host}")

        client = ollama.Client(host=ollama_host)
        response = client.list()

        # Handle the ListResponse object properly
        if hasattr(response, 'models'):
            models = response.models
        elif isinstance(response, dict) and 'models' in response:
            models = response['models']
        else:
            models = []

        print(f"  ✅ Connected to Ollama")
        print(f"  ✅ Found {len(models)} model(s):")
        for model in models[:5]:  # Show first 5
            model_name = model.model if hasattr(
                model, 'model') else model.get('model', 'unknown')
            param_size = model.details.parameter_size if hasattr(
                model, 'details') else model.get('details', {}).get('parameter_size', 'unknown')
            print(f"     - {model_name} ({param_size})")

        if len(models) == 0:
            print("  ⚠️  No models found. Run: ollama pull ministral-3:latest")
            return False

        return True
    except Exception as e:
        print(f"  ❌ Ollama connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ollama_inference():
    """Test actual LLM inference"""
    print("\n🧪 Testing Ollama inference...")
    import ollama

    try:
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[{
                'role': 'user',
                'content': 'Respond with exactly these three words: Environment is ready'
            }]
        )

        result = response['message']['content']
        print(f"  ✅ Inference successful")
        print(f"  Response: {result}")
        return True
    except Exception as e:
        print(f"  ❌ Inference failed: {e}")
        return False


def test_environment_variables():
    """Check critical environment variables"""
    print("\n🧪 Testing environment variables...")

    checks = {
        'PYTHONUNBUFFERED': '1',
        'PYTHONDONTWRITEBYTECODE': '1',
        'OLLAMA_HOST': None  # Just check it exists
    }

    passed = True
    for var, expected in checks.items():
        value = os.getenv(var)
        if value is None:
            print(f"  ⚠️  {var} not set")
            if var != 'OLLAMA_HOST':  # OLLAMA_HOST is optional
                passed = False
        elif expected and value != expected:
            print(f"  ⚠️  {var}={value} (expected {expected})")
        else:
            print(f"  ✅ {var}={value}")

    return passed


def test_file_structure():
    """Verify project structure"""
    print("\n🧪 Testing project structure...")

    required_files = [
        'pyproject.toml',
        '.devcontainer/devcontainer.json',
        '.devcontainer/Dockerfile',
        '.devcontainer/docker-compose.yml',
    ]

    recommended_files = [
        '.env.example',
        '.gitignore',
        'README.md',
    ]

    workspace = Path('/workspaces')
    passed = True

    for file in required_files:
        if (workspace / file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} missing")
            passed = False

    for file in recommended_files:
        if (workspace / file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} recommended but missing")

    return passed


def main():
    """Run all validation tests"""
    print("=" * 60)
    print("AI Engineering Lab - Environment Validation")
    print("=" * 60 + "\n")

    tests = [
        ("Package Imports", test_imports),
        ("Ollama Connection", test_ollama_connection),
        ("Ollama Inference", test_ollama_inference),
        ("Environment Variables", test_environment_variables),
        ("Project Structure", test_file_structure),
    ]

    results = []
    for name, test_func in tests:
        try:
            results.append(test_func())
        except Exception as e:
            print(f"\n❌ {name} crashed: {e}")
            results.append(False)
        print()

    # Summary
    print("=" * 60)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("🚀 Environment is ready for AI Engineering!")
        return 0
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total} passed)")
        print("Fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
