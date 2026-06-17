#!/usr/bin/env python3
"""
Unified smoke gate runner.

Usage:
  python smoke_gate.py --engine vllm --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0
  python smoke_gate.py --engine sglang --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0
  python smoke_gate.py --engine ollama --model gemma4 --gpu 0

Engines supported:
  vllm, sglang, ollama (extensible; add import + ENGINE_MAP entry)
"""

import argparse
import json
import time
import os
from datetime import datetime, timezone


def run_smoke(engine: str, model: str, gpu: int, timeout: float = 120.0) -> dict:
    result = {
        "meta": {
            "benchmark_suite": "smoke",
            "engine_name": engine,
            "engine_version": "unknown",
            "run_date": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "hardware": "TBD",
            "gpu_count": 1,
            "cuda_version": "TBD",
            "pytorch_version": "TBD",
            "model_id": model,
            "model_checkpoint_sha256": "TBD",
            "adapter_commit": "TBD",
            "harness_commit": "TBD",
            "judge_model": "N/A",
            "judge_prompt_sha256": "N/A",
        },
        "config": {
            "batching_config": {},
            "quantization": "fp16",
            "concurrency_levels": [1],
            "prompt_lengths": ["short"],
            "max_tokens": 32,
            "temperature": 0.0,
            "seed": 42,
        },
        "results": {
            "ttft": {"p50": 0.0, "p95": 0.0, "p99": 0.0, "unit": "ms"},
            "tpot": {"p50": 0.0, "p95": 0.0, "p99": 0.0, "unit": "ms"},
            "throughput": {"tokens_per_sec": 0.0, "requests_per_sec": 0.0},
            "gpu_utilization": {"mean": 0.0, "peak": 0.0, "unit": "%"},
            "gpu_memory": {"peak_mb": 0, "steady_mb": 0},
            "error_rate": 0.0,
            "total_requests": 0,
            "total_tokens": 0,
        },
        "per_request": [],
        "ops_notes": {
            "setup_time_sec": 0,
            "dependency_conflicts": 0,
            "undocumented_steps": 0,
            "cuda_version_mismatch": False,
            "model_conversion_required": False,
            "model_conversion_time_sec": 0,
            "status": "pending",
        },
    }

    t_setup = time.perf_counter()

    if engine == "vllm":
        from adapters.vllm_adapter import VLLMAdapter
        adapter = VLLMAdapter(model, gpu_devices=[gpu], port=8000)
    elif engine == "sglang":
        from adapters.sglang_adapter import SGLangAdapter
        adapter = SGLangAdapter(model, gpu_devices=[gpu], port=30000)
    elif engine == "ollama":
        from adapters.ollama_adapter import OllamaAdapter
        adapter = OllamaAdapter(model, gpu_devices=[gpu], port=11434)
    else:
        raise ValueError(f"Unknown engine: {engine}")

    adapter.setup()
    try:
        adapter.await_ready(timeout=timeout)
        t_ready = time.perf_counter() - t_setup
        result["ops_notes"]["setup_time_sec"] = round(t_ready, 1)

        # Turn 2: short prompt
        prompt = "Hello, what is 2+2?"
        resp = adapter.query(prompt, max_tokens=32, temperature=0.0)
        result["per_request"].append({
            "request_id": "smoke-001",
            "prompt_length": len(prompt),
            "ttft_ms": round(resp.ttft_ms, 2),
            "tpot_ms": round(resp.tpot_ms, 2),
            "total_tokens": resp.completion_tokens,
            "gpu_memory_mb": 0,
            "gpu_utilization_pct": 0,
            "error": None,
        })
        result["results"]["ttft"]["p50"] = round(resp.ttft_ms, 2)
        result["results"]["total_requests"] = 1
        result["results"]["total_tokens"] = resp.completion_tokens

        # Verify non-empty response
        assert resp.text.strip(), "Empty response"
        # Verify GPU utilization (best effort)
        telem = adapter.get_telemetry()
        if telem.gpu_utilization_pct and any(g > 0 for g in telem.gpu_utilization_pct):
            result["results"]["gpu_utilization"]["mean"] = round(
                sum(telem.gpu_utilization_pct) / len(telem.gpu_utilization_pct), 1
            )
            result["results"]["gpu_utilization"]["peak"] = max(telem.gpu_utilization_pct)
        else:
            print("WARNING: GPU utilization could not be measured or was 0%")

        result["ops_notes"]["status"] = "PASS"
        print(f"\n=== SMOKE GATE {engine.upper()}: PASS ===")
        print(f"  Setup time: {result['ops_notes']['setup_time_sec']:.1f}s")
        print(f"  TTFT: {resp.ttft_ms:.1f} ms")
        print(f"  Response: {resp.text[:80]}...")
    except Exception as e:
        result["ops_notes"]["status"] = f"FAIL: {e}"
        print(f"\n=== SMOKE GATE {engine.upper()}: FAIL ===")
        print(f"  Error: {e}")
    finally:
        adapter.teardown()

    # Save result
    out_dir = os.path.join(os.path.dirname(__file__), "benchmarks")
    os.makedirs(out_dir, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = os.path.join(out_dir, f"smoke-{engine}-{date_str}.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"  Result saved: {out_path}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smoke gate runner")
    parser.add_argument("--engine", required=True, choices=["vllm", "sglang", "ollama"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()
    run_smoke(args.engine, args.model, args.gpu, args.timeout)
