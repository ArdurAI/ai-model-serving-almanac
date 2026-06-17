# Smoke Gate Runner

Runs the three-turn smoke gate for every engine on the Tier A roster.
The smoke gate is the minimum bar for an engine to be officially "in" the almanac.

## Three-turn scenario

```
Turn 1: Deploy the engine with a standard model (Llama-3.1-8B-Instruct or equivalent)
Turn 2: Send a standard chat completion request (mixed prompt: short + medium + long)
Turn 3: Verify the response is non-empty, JSON-schema-compliant, and GPU was utilized
```

## Pass criteria

- No crashes, no silent failures, no CUDA OOM during the basic test
- Response must be non-empty and structurally valid (has `choices[0].text` or `choices[0].message.content` or native equivalent)
- GPU must show utilization > 0% during generation (verifies the engine actually used the GPU, not CPU fallback)
- Engine must handle the basic case without workarounds or undocumented flags

## Usage

```bash
# Run smoke gate for a single engine
python -m adapters.vllm_adapter --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0

# Or use the unified runner
python smoke_gate.py --engine vllm --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0
```

## Results

Results are written to `benchmarks/smoke-<engine>-<date>.json` following the
standard benchmark schema (see `benchmarks/README.md`).
