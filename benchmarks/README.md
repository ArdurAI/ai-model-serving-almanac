# Benchmarks Directory

This directory contains raw benchmark results for every engine on the roster. Results are **never overwritten** — only appended. Each file is an immutable record of a specific benchmark run.

## Naming Convention

```
<benchmark-suite>-<engine-name>-<YYYY-MM-DD>.json
<benchmark-suite>-<engine-name>-<YYYY-MM-DD>.md
```

Examples:
- `llmperf-vllm-2026-06-16.json` — LLMPerf benchmark results for vLLM
- `anyscale-sglang-2026-06-16.json` — AnyScale serving benchmark for SGLang
- `throughput-tensorrt-llm-2026-06-16.json` — Custom throughput benchmark for TensorRT-LLM

## Benchmark Suites

| Suite | What it measures | File prefix |
|-------|-----------------|-------------|
| **LLMPerf** | TTFT, TPOT, throughput, inter-token latency under load | `llmperf-` |
| **AnyScale** | Sustained throughput, goodput, error rate under sustained load | `anyscale-` |
| **MMLU** | Accuracy retention under quantization vs. reference fp16 | `mmlu-` |
| **GSM8K** | Math reasoning accuracy retention under quantization | `gsm8k-` |
| **Perplexity** | Perplexity delta vs. reference fp16 after quantization | `perplexity-` |
| **Logits divergence** | KL divergence of output distributions vs. reference fp16 | `logits-` |
| **Throughput** | Custom PlatformOps throughput benchmark | `throughput-` |
| **Stress** | Stress suite results (prefill-decode, concurrent flood, KV exhaustion, etc.) | `stress-` |
| **Smoke gate** | Smoke gate pass/fail results | `smoke-` |
| **Ops burden** | Setup time, dependency conflicts, upgrade pain | `ops-` |

## JSON Schema

Every benchmark result file follows this schema:

```json
{
  "meta": {
    "benchmark_suite": "llmperf",
    "engine_name": "vllm",
    "engine_version": "0.6.0",
    "run_date": "2026-06-16T14:30:00Z",
    "hardware": "A100-80GB",
    "gpu_count": 1,
    "cuda_version": "12.4",
    "pytorch_version": "2.3.0",
    "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "model_checkpoint_sha256": "abc123...",
    "adapter_commit": "a1b2c3d",
    "harness_commit": "e4f5g6h",
    "judge_model": "claude-opus-4-8",
    "judge_prompt_sha256": "sha256:..."
  },
  "config": {
    "batching_config": { ... },
    "quantization": "fp16",
    "concurrency_levels": [1, 2, 4, 8, 16, 32, 64],
    "prompt_lengths": ["short", "medium", "long"],
    "max_tokens": 256,
    "temperature": 0.0,
    "seed": 42
  },
  "results": {
    "ttft": { "p50": 12.3, "p95": 45.6, "p99": 78.9, "unit": "ms" },
    "tpot": { "p50": 8.7, "p95": 15.2, "p99": 22.1, "unit": "ms" },
    "throughput": { "tokens_per_sec": 1234.5, "requests_per_sec": 45.6 },
    "gpu_utilization": { "mean": 87.3, "peak": 98.1, "unit": "%" },
    "gpu_memory": { "peak_mb": 16384, "steady_mb": 14336 },
    "error_rate": 0.0,
    "total_requests": 1000,
    "total_tokens": 256000
  },
  "per_request": [
    {
      "request_id": "req-001",
      "prompt_length": 128,
      "ttft_ms": 12.5,
      "tpot_ms": 8.9,
      "total_tokens": 256,
      "gpu_memory_mb": 14336,
      "gpu_utilization_pct": 87.5,
      "error": null
    }
  ],
  "ops_notes": {
    "setup_time_sec": 120,
    "dependency_conflicts": 0,
    "undocumented_steps": 1,
    "cuda_version_mismatch": false,
    "model_conversion_required": false,
    "model_conversion_time_sec": 0
  }
}
```

## License

Benchmark data is licensed CC BY 4.0.
