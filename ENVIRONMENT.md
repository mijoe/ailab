# AI Lab Environment Documentation

**Last Updated:** 2026-02-16  
**Maintainer:** Michael Jörg

---

## Hardware Configurations

### Work Laptop (Development & Learning)

**System:** Linux (native, not WSL)  
**GPU:** NVIDIA RTX A500 Laptop GPU  
**VRAM:** 4GB  
**CUDA Cores:** ~2,048  
**TDP:** 30W  
**Driver Version:** 535.288.01  
**CUDA Version:** 12.2

**Primary Use Cases:**
- Development and testing
- Small model experimentation (≤3B parameters)
- Learning and hands-on exercises
- Prompt engineering practice
- RAG system prototyping

**Constraints:**
- 4GB VRAM limit (strict bottleneck)
- Laptop thermal management (sustained loads)
- Corporate network restrictions
- Professional work environment

**Recommended Models:**
- ✅ Llama 3.2 3B (Q4): ~2.5GB VRAM
- ✅ Ministral 3B: ~2GB VRAM  
- ✅ Phi-3 Mini: ~2GB VRAM
- ✅ All-MiniLM-L6-v2 (embeddings): ~100MB
- ⚠️ Mistral 7B (Q4): ~4.5GB VRAM (tight, test first)
- ❌ Llama 3.2 11B+: Insufficient VRAM

---

### Home Workstation (Heavy Lifting)

**System:** Windows 11 + WSL2 (Ubuntu)  
**Kernel:** 6.6.87.2-microsoft-standard-WSL2  
**GPU:** NVIDIA GeForce RTX 5080  
**VRAM:** 16,303 MiB (~16GB)  
**CUDA Cores:** 10,752 (Blackwell architecture)  
**TDP:** 360W  
**Driver Version:** 591.86 (Windows host) / 590.57 (WSL2 passthrough)  
**CUDA Version:** 13.1  
**Architecture:** Blackwell (5th gen RTX)

**WSL2 GPU Notes:**
- GPU accessed via Windows driver passthrough
- No separate Linux driver installation needed
- CUDA Toolkit available through WSL2 integration
- DirectML and CUDA both supported

**Primary Use Cases:**
- Fine-tuning experiments (7B-70B models)
- Large model testing and evaluation
- Batch processing and data preparation
- Multi-model experiments
- Production-scale prototyping
- Extended training runs
- Parallel inference workloads

**Capabilities:**
- ✅ Models up to 70B parameters (Q4 quantized)
- ✅ Fine-tuning 7B-13B models (full precision)
- ✅ Fine-tuning 30B+ models (quantized)
- ✅ Multiple concurrent model instances (2-3 small models)
- ✅ Large batch sizes for embeddings and data processing
- ✅ Full-precision 13B model inference
- ⚠️ 70B+ models: Require quantization (Q3-Q4)
- ⚠️ Training from scratch: Limited to smaller models (<1B)

**Recommended Models:**
- ✅ Llama 3.2 11B (full precision)
- ✅ Llama 3.1 70B (Q4 quantized, ~40GB)
- ✅ Mistral 7B (full precision + fine-tuning)
- ✅ Mixtral 8x7B (Q4 quantized)
- ✅ Code Llama 34B (Q4-Q5 quantized)
- ✅ DeepSeek Coder 33B (Q4 quantized)
- ⚠️ Llama 3.1 405B (Q2 only, experimental)
- ⚠️ Multiple 7B models concurrent (2-3 max)

---

## Software Stack

### Core Development Tools

**Container Runtime:**
- Docker + Docker Compose
- NVIDIA Container Toolkit (work laptop: installed 2026-02-16)
- Dev Containers extension for VS Code

**IDE:**
- Visual Studio Code
- Dev Containers extension
- Python extension
- Remote development support

**Python Environment:**
- Python 3.11+ (in container)
- uv package manager (preferred over pip)
- Virtual environments via uv

**AI Infrastructure:**
- Ollama (latest) - local model inference
- LangChain - orchestration framework
- ChromaDB / FAISS - vector stores (TBD based on project needs)

---

## WSL2 GPU Configuration (Home Workstation)

### How GPU Passthrough Works

**Architecture:**
```
Windows Host (Driver 591.86)
    ↓
WSL2 Virtual Machine (Kernel 6.6.87.2)
    ↓
NVIDIA Container Toolkit
    ↓
Docker Containers (CUDA 13.1)
    ↓
Ollama / PyTorch / TensorFlow
```

**Key Differences from Native Linux:**
- Windows driver handles GPU (no separate Linux driver)
- GPU accessible via `/dev/dxg` device
- CUDA forwarded through WSL2 integration
- Memory shared between Windows and WSL2 (not isolated)

### Setup Requirements

**Already Configured (Assumed):**
- ✅ WSL2 installed and updated
- ✅ NVIDIA GPU driver on Windows (591.86)
- ✅ CUDA support enabled in WSL2
- ✅ Docker Desktop with WSL2 backend

**To Verify:**
```bash
# Check WSL2 can see GPU
nvidia-smi

# Check CUDA available
nvcc --version  # May need CUDA toolkit installed

# Check Docker GPU access
docker run --rm --gpus all nvidia/cuda:13.1.0-base-ubuntu22.04 nvidia-smi
```

**If GPU Not Working in Docker:**
```bash
# Install NVIDIA Container Toolkit in WSL2
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker  # Or restart Docker Desktop
```

### WSL2-Specific Considerations

**Performance:**
- ⚠️ ~5-10% overhead vs native Linux (acceptable)
- ⚠️ File I/O slower on Windows drives (`/mnt/c/`)
- ✅ Keep all project files in WSL2 filesystem (`~/Code/`)
- ✅ GPU compute performance nearly identical to native

**Memory Management:**
- WSL2 shares system RAM with Windows
- Default: WSL2 can use 50% of total RAM
- GPU VRAM: Fully accessible (16GB)
- Can configure in `.wslconfig` if needed

**Networking:**
- WSL2 has separate IP from Windows
- Localhost forwarding works automatically
- Docker ports accessible from Windows
- Ollama API: `http://localhost:11434` works from both

**File System:**
- ⚠️ `/mnt/c/` (Windows drives): Slow, avoid for Docker volumes
- ✅ `~/` (WSL2 filesystem): Fast, use for all AI work
- ✅ Docker volumes: Stored in WSL2, good performance

### Recommended WSL2 Configuration

**File: `C:\Users\[YourUser]\.wslconfig` (Windows side)**
```ini
[wsl2]
# Allow WSL2 to use up to 32GB RAM (adjust based on total RAM)
memory=32GB

# Limit WSL2 to 12 CPU cores (leave some for Windows)
processors=12

# Enable nested virtualization (for Docker)
nestedVirtualization=true

# Swap configuration
swap=8GB
swapFile=C:\\Users\\[YourUser]\\wsl-swap.vhdx
```

**Apply changes:**
```powershell
# In PowerShell (as Admin)
wsl --shutdown
# Restart WSL2
```

### WSL2 Troubleshooting

**GPU Not Visible in WSL2:**
1. Update Windows NVIDIA driver (GeForce Experience)
2. Update WSL2: `wsl --update`
3. Restart WSL2: `wsl --shutdown` then reopen terminal
4. Check Windows driver supports WSL2 GPU passthrough

**Docker Can't Access GPU:**
1. Verify Docker Desktop using WSL2 backend (Settings → General)
2. Install NVIDIA Container Toolkit in WSL2 (see above)
3. Restart Docker Desktop
4. Test: `docker run --rm --gpus all nvidia/cuda:13.1.0-base-ubuntu22.04 nvidia-smi`

**Slow Performance:**
1. Ensure project files in WSL2 filesystem (`~/Code/`), not `/mnt/c/`
2. Check `.wslconfig` memory allocation
3. Close memory-heavy Windows applications
4. Monitor GPU usage: `nvidia-smi -l 1`

**Network Issues:**
1. Check Windows Firewall (may block WSL2 → Windows connections)
2. Verify Docker Desktop networking settings
3. Use `localhost` for Ollama, not WSL2 IP

---

## Development Environment

### Container Configuration

**Location:** `/workspaces` (inside container)  
**Persistence:** Docker volumes for Ollama models  
**Network:** Service networking (app ↔ ollama)

**Key Features:**
- GPU passthrough to Ollama service
- Shared volumes for code and data
- Isolated Python environment
- Pre-configured tools and libraries

**GPU Detection:**
- Work laptop (native Linux): Automatic via NVIDIA Container Toolkit
- Home workstation (WSL2): Automatic via Windows driver passthrough + Container Toolkit
- CPU fallback: Manual (comment out deploy section in docker-compose.yml)

**Platform-Specific Notes:**
- WSL2: Ensure Docker Desktop using WSL2 backend
- WSL2: Keep project files in `~/` not `/mnt/c/` for performance
- Native Linux: Direct GPU access, no Windows overhead

### Environment Variables

```bash
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
OLLAMA_HOST=http://localhost:11434
```

### Validation

Run environment checks:
```bash
uv run validate_environment.py
```

Expected output: All tests passing (5/5)

---

## Model Size Guidelines

### General Rules

| Model Size | Work Laptop (4GB) | Home Workstation (16GB) |
|-----------|-------------------|-------------------------|
| <3B params | ✅ Smooth | ✅ Instant |
| 3-7B params | ⚠️ Tight | ✅ Smooth (full precision) |
| 7-13B params | ❌ OOM | ✅ Excellent (full precision) |
| 13-34B params | ❌ No chance | ✅ Good (Q4-Q6 quantized) |
| 34-70B params | ❌ No chance | ⚠️ Q3-Q4 quantized only |
| 70B+ params | ❌ No chance | ⚠️ Q2-Q3, very tight |
| 405B params | ❌ No chance | ❌ Cloud recommended |

### Quantization Impact

**GGUF Quantization Levels (approximate):**
- Q2: ~2.5GB per 7B model (quality loss)
- Q4: ~4GB per 7B model (good balance)
- Q5: ~5GB per 7B model (minimal loss)
- Q8: ~8GB per 7B model (near full quality)
- F16: ~14GB per 7B model (full precision)

**Work laptop strategy:** Stick to Q4 for 3B models, Q2-Q3 if testing 7B  
**Home workstation strategy:** Q4-Q5 for 7B-13B, Q2-Q3 for larger models

---

## Security Boundaries

### Work Laptop (Corporate Device)

**STRICT RULES:**
- ❌ No production API keys
- ❌ No customer/sensitive data
- ❌ No credential storage in repos
- ✅ Personal learning projects only
- ✅ Public datasets acceptable
- ✅ Synthetic/example data preferred

**Data Handling:**
- All secrets in `.env` (gitignored)
- No PII in training data
- No proprietary company information
- Treat all outputs as potentially logged

**Network Considerations:**
- Corporate firewall rules apply
- Model downloads may be restricted
- API endpoints may be blocked
- Use approved repositories only

### Home Workstation

**MORE FLEXIBLE:**
- ✅ Personal API keys (secured)
- ✅ Larger datasets
- ✅ Longer experiments
- ⚠️ Still no real customer data
- ⚠️ Follow data protection best practices

**Security Practices:**
- API keys in environment variables
- Separate .env files per project
- Encrypted storage for sensitive configs
- Regular credential rotation
- Network isolation for experiments

---

## Attack Surface Analysis

### Container Security

**GPU Passthrough Risks:**
- Kernel-level NVIDIA drivers exposed
- GPU memory not cleared between runs
- Potential data leakage across containers
- Weaker container isolation

**Mitigation:**
- Regular driver updates
- Separate environments for different trust levels
- No sensitive data in model fine-tuning
- Monitor GPU memory usage

### Model Security

**Prompt Injection Vectors:**
- User inputs (untrusted by default)
- Retrieved documents (RAG sources)
- Function calling arguments
- System prompt overrides

**Defense Layers:**
- Input validation and sanitization
- Output filtering
- Role-based access controls
- Audit logging for model interactions

### Data Security

**Training Data:**
- Never include passwords, API keys, PII
- Sanitize all datasets before use
- Document data sources and licenses
- Version control for reproducibility

**Model Outputs:**
- Treat as potentially leaked
- No sensitive data in prompts
- Filter outputs before storage
- Assume adversarial users

---

## Performance Expectations

### Work Laptop (RTX A500)

**Inference Speed (Ministral 3B, Q4):**
- First token: ~500ms
- Tokens/second: 50-100
- Batch size: 1-4
- Context window: Full 8K usable

**Embedding Generation:**
- Sentences/second: 100-200
- Documents/minute: 500-1000
- Batch processing: Limited by VRAM

**Model Loading:**
- 3B model: 5-10 seconds
- Model switching: 3-5 seconds
- Cold start penalty: +2-3 seconds

### Home Workstation (RTX 5080)

**Inference Speed (Llama 3.2 11B, FP16):**
- First token: ~200-300ms
- Tokens/second: 150-250 (full precision)
- Tokens/second: 250-400 (Q4 quantized)
- Batch size: 8-16
- Context window: Full 128K usable (with proper attention optimization)

**Inference Speed (Llama 3.1 70B, Q4):**
- First token: ~800ms-1.2s
- Tokens/second: 40-80
- Batch size: 1-2
- Context window: 32K-64K practical limit

**Embedding Generation:**
- Sentences/second: 500-1000
- Documents/minute: 5000-10000
- Batch processing: 256-512 batch size

**Model Loading:**
- 7B model: 2-3 seconds
- 13B model: 3-5 seconds
- 70B model (Q4): 10-15 seconds
- Model switching: 1-2 seconds
- Cold start penalty: +1-2 seconds

**Fine-tuning Estimates (LoRA):**
- 7B model: ~30-60 min/epoch (small dataset <10K examples)
- 13B model: ~60-120 min/epoch
- Batch size: 4-8 for 7B, 2-4 for 13B

**Performance vs Work Laptop:**
- ~5-6x faster inference (11B model comparison)
- ~4x larger batch sizes
- Can run models 4x larger
- 2-3 concurrent models possible (vs 1)

---

## Known Issues & Workarounds

### Work Laptop

**Issue:** Container fails to start with GPU error  
**Cause:** NVIDIA Container Toolkit not installed  
**Solution:** See installation docs (completed 2026-02-16)

**Issue:** Model runs on CPU despite GPU available  
**Cause:** Docker compose deploy section missing  
**Solution:** Verify `deploy.resources.reservations.devices` configured

**Issue:** OOM when loading 7B models  
**Cause:** 4GB VRAM insufficient  
**Solution:** Use 3B models or switch to home workstation

### Home Workstation (WSL2)

**Issue:** GPU not visible in `nvidia-smi` within WSL2  
**Cause:** Windows NVIDIA driver not WSL2-compatible or outdated  
**Solution:** Update Windows GPU driver to latest version (591.86+), run `wsl --update`, restart WSL2

**Issue:** Docker can't access GPU despite `nvidia-smi` working  
**Cause:** NVIDIA Container Toolkit not installed in WSL2  
**Solution:** Install toolkit in WSL2 environment (see WSL2 GPU Configuration section)

**Issue:** Slow file I/O and model loading  
**Cause:** Project files on Windows filesystem (`/mnt/c/`)  
**Solution:** Move all AI projects to WSL2 home directory (`~/Code/AI/`)

**Issue:** Docker containers fail to start with "not enough memory"  
**Cause:** WSL2 memory limit too low in `.wslconfig`  
**Solution:** Increase memory allocation, restart WSL2 (`wsl --shutdown`)

**Issue:** Models load slowly compared to native Linux  
**Cause:** Expected ~5-10% overhead in WSL2  
**Solution:** Accept overhead or dual-boot native Linux (overkill for most use cases)

---

## Migration Between Environments

### Work → Home Transfer

**Code & Configs:**
```bash
# Git push from work laptop
git push origin feature-branch

# Git pull on home workstation  
git pull origin feature-branch
```

**Models:**
- Don't transfer - re-download on each system
- Ollama models stored in Docker volumes
- Use same model tags for consistency

**Data & Results:**
- Export results as artifacts
- Use cloud storage for large datasets
- Version control for experiment configs

### Reproducibility Checklist

- [ ] Model version documented
- [ ] Quantization level specified  
- [ ] Seed values recorded
- [ ] Temperature/parameters logged
- [ ] Dataset version tracked
- [ ] Environment variables noted

---

## Maintenance

### Regular Updates

**Weekly:**
- Check for Ollama updates
- Pull latest model versions for active projects
- Review container logs for errors

**Monthly:**
- Update NVIDIA drivers (if stable)
- Update Docker and Container Toolkit
- Clean unused models: `ollama rm <model>`
- Prune Docker volumes: `docker volume prune`

**Quarterly:**
- Review and update this document
- Audit installed models and usage
- Check for security advisories
- Update Python dependencies

### Health Checks

**Quick validation:**
```bash
# GPU accessible
nvidia-smi

# Docker GPU runtime working
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi

# Ollama healthy
curl http://localhost:11434/api/tags

# Environment tests pass
uv run validate_environment.py
```

---

## Learning Path Context

This environment supports the 12-week AI Engineering learning program:

**Weeks 1-4:** Foundations + RAG  
- Work laptop sufficient
- Small models (3B) adequate
- Focus on concepts, not scale

**Weeks 5-8:** Evaluation + Agents + Production  
- Work laptop primary
- Home for larger experiments
- Multi-model testing

**Weeks 9-12:** Fine-tuning + Optimization  
- Home workstation required
- GPU memory critical
- Larger datasets needed

**Current Status:** Week 1 complete, Week 2 starting (2026-02-16)

---

## Emergency Procedures

### GPU Not Detected

1. Check driver: `nvidia-smi`
2. Check Docker runtime: `docker info | grep -i runtime`
3. Restart Docker: `sudo systemctl restart docker`
4. Rebuild container: `docker compose down && docker compose up --build`

### Container Won't Start

1. Check logs: `docker compose logs ollama`
2. Verify GPU config in docker-compose.yml
3. Test with CPU-only (comment out deploy section)
4. Check disk space: `df -h`

### Model Inference Hangs

1. Check GPU memory: `nvidia-smi`
2. Kill hung process: `docker compose restart ollama`
3. Reduce batch size or model size
4. Check Ollama logs: `docker compose logs -f ollama`

### Fallback to CPU

If GPU issues persist and work is blocked:

```yaml
# In docker-compose.yml, comment out:
# deploy:
#   resources:
#     reservations:
#       devices:
#         - driver: nvidia
#           count: all
#           capabilities: [gpu]
```

Expect 5-10x slower inference, but environment remains functional.

---

## Additional Resources

**Documentation:**
- NVIDIA Container Toolkit: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/
- Ollama API: https://github.com/ollama/ollama/blob/main/docs/api.md
- LangChain Docs: https://python.langchain.com/

**Model Repositories:**
- Ollama Library: https://ollama.com/library
- Hugging Face: https://huggingface.co/models

**Security References:**
- OWASP LLM Top 10: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Prompt Injection Guide: [TODO: Add after Ch 5]

---

## Changelog

**2026-02-16 (Evening - Home Workstation):**
- ✅ Added RTX 5080 specifications (16GB VRAM, 10,752 CUDA cores)
- ✅ Documented WSL2 GPU passthrough architecture
- ✅ Added WSL2-specific configuration and troubleshooting
- ✅ Updated performance benchmarks for 16GB VRAM
- ✅ Expanded model size guidelines (up to 70B parameters)
- ✅ Added fine-tuning performance estimates
- ✅ Documented known WSL2 issues and solutions

**2026-02-16 (Afternoon - Work Laptop):**
- Initial documentation created
- Work laptop GPU configuration verified (RTX A500, 4GB VRAM)
- NVIDIA Container Toolkit installed and tested
- Environment validation passing (5/5 tests)
- Home workstation section scaffolded

**[Future updates will be logged here]**