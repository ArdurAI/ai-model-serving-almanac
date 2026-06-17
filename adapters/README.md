# Benchmark Adapters

This directory contains the adapter layer that connects the benchmark harness to individual inference engines. Every engine on the roster must satisfy the `ModelServingAdapter` interface to enter the standard benchmark pipeline.

## Adapter Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Benchmark      │────▶│  Adapter     │────▶│  Engine Process │
│  Harness        │     │  (this dir)  │     │  (subprocess)   │
│  (llmperf_      │     │              │     │                 │
│   runner.py)    │     │  Standardized│     │  vllm serve     │
│                 │     │  Response    │     │  sglang ...     │
│                 │     │  Telemetry   │     │  ollama serve   │
│                 │     │  Lifecycle   │     │  ...            │
└─────────────────┘     └──────────────┘     └─────────────────┘
```

The adapter is the **only** per-engine code that changes. The harness, prompts, judge, and scoring rubric are fixed.

## Files

| File | Purpose | Engines covered |
|------|---------|-----------------|
| `__init__.py` | Base `ModelServingAdapter` contract, `Response`, `Telemetry` dataclasses | All |
| `llmperf_adapter.py` | `LLMPerfAdapter` — OpenAI-compatible HTTP adapter | vLLM, SGLang, TGI, LMDeploy, llama.cpp (llama-server) |
| `anyscale_adapter.py` | `AnyScaleAdapter` — sustained load / goodput testing | Any OpenAI-compatible engine |
| `custom_adapter.py` | `CustomServingAdapter` — base for non-OpenAI engines | TensorRT-LLM (Python API), NVIDIA Dynamo, edge runtimes |
| `vllm_adapter.py` | Concrete vLLM adapter + smoke gate | vLLM |
| `sglang_adapter.py` | Concrete SGLang adapter + smoke gate | SGLang |
| `ollama_adapter.py` | Concrete Ollama adapter + smoke gate | Ollama |
| `lmdeploy_adapter.py` | Concrete LMDeploy adapter + smoke gate | LMDeploy |
| `llamacpp_adapter.py` | Concrete llama.cpp adapter + smoke gate | llama.cpp (llama-server) |
| `tensorrtllm_adapter.py` | Concrete TensorRT-LLM adapter (Python API + Triton) | TensorRT-LLM |

## Adding a New Adapter

1. **Subclass the right base class**:
   - If the engine has an OpenAI-compatible REST API → subclass `LLMPerfAdapter`
   - If the engine has a custom protocol (gRPC, custom HTTP, binary) → subclass `CustomServingAdapter`
   - If you need sustained load testing → subclass `AnyScaleAdapter` (or add `run_sustained_load()` to your adapter)

2. **Implement the lifecycle methods**:
   ```python
   class MyEngineAdapter(LLMPerfAdapter):
       def setup(self):
           # Launch the engine subprocess
           pass
       
       def await_ready(self, timeout=300.0):
           # Poll health endpoint, send warm-up request
           pass
       
       def teardown(self):
           # Kill subprocess, clean up GPU memory
           pass
   ```

3. **Register the engine** in `ENGINE_MAP` in `llmperf_runner.py` and `sustained_load_runner.py`.

4. **Add a smoke gate** at the bottom of the adapter file so it can be run standalone:
   ```bash
   python -m adapters.myengine_adapter --model my-model --gpu 0
   ```

5. **Run the smoke gate** before submitting the adapter:
   ```bash
   python -m adapters.myengine_adapter --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0
   ```

## Smoke Gate

Every adapter must pass the three-turn smoke gate:

1. **Turn 1**: Deploy the engine with a standard model
2. **Turn 2**: Send a standard chat completion request (short + medium + long prompt)
3. **Turn 3**: Verify response is non-empty, structurally valid, and GPU was utilized

Run the unified smoke gate:

```bash
# Supported engines: vllm, sglang, ollama, lmdeploy, llamacpp
python smoke_gate.py --engine vllm --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0
```

Or run the adapter's standalone smoke gate:

```bash
python -m adapters.vllm_adapter --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0
python -m adapters.sglang_adapter --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0
python -m adapters.ollama_adapter --model gemma4 --gpu 0
python -m adapters.lmdeploy_adapter --model internlm/internlm2-chat-7b --gpu 0 --backend turbomind
python -m adapters.llamacpp_adapter --model ./models/llama-3.1-8b-q4_k_m.gguf --gpu 0 --ngl 33
python -m adapters.tensorrtllm_adapter --model meta-llama/Meta-Llama-3.1-8B-Instruct --mode python --gpu 0
```

## LLMPerf Benchmark

Run the LLMPerf benchmark across multiple concurrency levels:

```bash
python llmperf_runner.py \
  --engine vllm \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --gpu 0 \
  --concurrency 1,2,4,8,16,32 \
  --max-tokens 256
```

Results are saved to `benchmarks/llmperf-<engine>-<date>.json`.

## Sustained Load Benchmark

Run the AnyScale-style sustained load test:

```bash
python sustained_load_runner.py \
  --engine vllm \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --gpu 0 \
  --concurrency 16 \
  --duration 60 \
  --max-tokens 256
```

Results are saved to `benchmarks/anyscale-<engine>-<date>.json`.

## Adapter Contract (Frozen)

```python
class ModelServingAdapter(ABC):
    def setup(self) -> None: ...          # Install, configure, start engine
    def load(self, model_path, ...) -> None: ...  # Load model weights
    def await_ready(self, timeout) -> None: ...   # Wait for health + warm-up
    def query(self, prompt, max_tokens, ...) -> Response: ...  # Single request
    def batch_query(self, prompts, ...) -> List[Response]: ...  # Concurrent
    def teardown(self) -> None: ...       # Clean up, kill processes
    def get_telemetry(self) -> Telemetry: ...  # GPU / system telemetry
```

**Do NOT modify the interface without an RFC and public announcement.**
See `TESTING.md` § Methodology changes.

## License

Adapter code is MIT-licensed. See `../INTENT.md` for almanac content licensing.
