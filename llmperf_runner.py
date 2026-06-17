#!/usr/bin/env python3
"""
LLMPerf Benchmark Runner — unified per-request latency and throughput benchmark.

Usage:
  python llmperf_runner.py --engine vllm --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0 --concurrency 1,2,4,8,16,32
  python llmperf_runner.py --engine sglang --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0 --concurrency 1,4,16
  python llmperf_runner.py --engine ollama --model gemma4 --gpu 0 --concurrency 1,2,4

Produces a JSON result file in benchmarks/llmperf-<engine>-<date>.json
following the schema documented in benchmarks/README.md.
"""

import argparse
import json
import os
import time
import statistics
from datetime import datetime, timezone
from typing import List, Dict, Any

# Engine -> adapter module mapping
ENGINE_MAP = {
    "vllm": "adapters.vllm_adapter",
    "sglang": "adapters.sglang_adapter",
    "ollama": "adapters.ollama_adapter",
    "lmdeploy": "adapters.lmdeploy_adapter",
    "llamacpp": "adapters.llamacpp_adapter",
}


def make_adapter(engine: str, model: str, gpu: int, **kwargs):
    """Import and instantiate the correct adapter for the engine."""
    mod_name = ENGINE_MAP.get(engine)
    if not mod_name:
        raise ValueError(f"Unknown engine: {engine}. Known: {list(ENGINE_MAP.keys())}")
    mod = __import__(mod_name, fromlist=["Adapter"])
    if engine == "vllm":
        return mod.VLLMAdapter(model, gpu_devices=[gpu], port=kwargs.get("port", 8000))
    elif engine == "sglang":
        return mod.SGLangAdapter(model, gpu_devices=[gpu], port=kwargs.get("port", 30000))
    elif engine == "ollama":
        return mod.OllamaAdapter(model, gpu_devices=[gpu], port=kwargs.get("port", 11434))
    elif engine == "lmdeploy":
        return mod.LMDeployAdapter(model, gpu_devices=[gpu], port=kwargs.get("port", 23333))
    elif engine == "llamacpp":
        return mod.LlamaCppAdapter(model, gpu_devices=[gpu], port=kwargs.get("port", 8080))
    else:
        raise ValueError(f"No adapter constructor for engine: {engine}")


PROMPTS = {
    "short": "What is 2+2?",
    "medium": "Explain the difference between prefill and decode phases in LLM inference, in one paragraph.",
    "long": (
        "You are a helpful assistant. Please summarize the following technical document about "
        "model serving optimization techniques. Include key points about KV cache management, "
        "continuous batching, speculative decoding, and quantization. Keep it under 200 words.\n\n"
        "[Document: Model serving at scale requires careful optimization of memory bandwidth and compute. "
        "The KV cache stores key and value tensors for each token during autoregressive generation. "
        "PagedAttention improves memory efficiency by storing KV cache in non-contiguous blocks. "
        "Continuous batching allows new requests to join an ongoing batch without waiting for the entire "
        "batch to finish. Speculative decoding uses a smaller draft model to generate candidate tokens "
        "that are verified by the larger target model. Quantization reduces model size and memory bandwidth "
        "by using lower precision weights and activations. Common formats include INT8, INT4, FP8, and "
        "various GGUF quantization schemes. Each technique trades off accuracy, latency, and throughput "
        "depending on the hardware target and model architecture.]"
    ),
}


def run_llmperf(
    engine: str,
    model: str,
    gpu: int,
    concurrency_levels: List[int],
    max_tokens: int = 256,
    temperature: float = 0.0,
    port: int = None,
    timeout: float = 300.0,
) -> Dict[str, Any]:
    """Run LLMPerf-style benchmark across multiple concurrency levels."""
    
    adapter_kwargs = {"port": port} if port else {}
    adapter = make_adapter(engine, model, gpu, **adapter_kwargs)
    
    result = {
        "meta": {
            "benchmark_suite": "llmperf",
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
            "concurrency_levels": concurrency_levels,
            "prompt_lengths": list(PROMPTS.keys()),
            "max_tokens": max_tokens,
            "temperature": temperature,
            "seed": 42,
        },
        "results": {},
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
    
    t0_setup = time.perf_counter()
    adapter.setup()
    try:
        adapter.await_ready(timeout=timeout)
        t_setup = time.perf_counter() - t0_setup
        result["ops_notes"]["setup_time_sec"] = round(t_setup, 1)
        
        for conc in concurrency_levels:
            print(f"\n--- Concurrency = {conc} ---")
            
            # Cycle through prompt lengths
            prompts = [PROMPTS[k] for k in ["short", "medium", "long"]]
            batch_prompts = []
            for i in range(conc):
                batch_prompts.append(prompts[i % len(prompts)])
            
            # Run batch query
            t_batch_start = time.perf_counter()
            responses = adapter.batch_query(batch_prompts, max_tokens=max_tokens, temperature=temperature)
            t_batch_total = time.perf_counter() - t_batch_start
            
            # Collect metrics
            ttfts = [r.ttft_ms for r in responses if r.ttft_ms > 0]
            tpots = [r.tpot_ms for r in responses if r.tpot_ms > 0]
            tokens = [r.completion_tokens for r in responses]
            total_tokens = sum(tokens)
            
            # Telemetry snapshot
            telem = adapter.get_telemetry()
            gpu_util = telem.gpu_utilization_pct
            gpu_mem = telem.gpu_memory_used_mb
            
            result["results"][f"concurrency_{conc}"] = {
                "ttft_p50_ms": round(statistics.median(ttfts), 2) if ttfts else 0.0,
                "ttft_p95_ms": round(statistics.quantiles(ttfts, n=20)[18], 2) if len(ttfts) >= 20 else (max(ttfts) if ttfts else 0.0),
                "ttft_p99_ms": round(statistics.quantiles(ttfts, n=100)[98], 2) if len(ttfts) >= 100 else (max(ttfts) if ttfts else 0.0),
                "tpot_p50_ms": round(statistics.median(tpots), 2) if tpots else 0.0,
                "tpot_p95_ms": round(statistics.quantiles(tpots, n=20)[18], 2) if len(tpots) >= 20 else (max(tpots) if tpots else 0.0),
                "throughput_tokens_per_sec": round(total_tokens / t_batch_total, 2) if t_batch_total > 0 else 0.0,
                "requests_per_sec": round(conc / t_batch_total, 2) if t_batch_total > 0 else 0.0,
                "gpu_utilization_mean_pct": round(sum(gpu_util) / len(gpu_util), 1) if gpu_util else 0.0,
                "gpu_utilization_peak_pct": max(gpu_util) if gpu_util else 0.0,
                "gpu_memory_peak_mb": max(gpu_mem) if gpu_mem else 0,
                "total_requests": conc,
                "total_tokens": total_tokens,
                "error_count": sum(1 for r in responses if not r.text.strip()),
            }
            
            for i, r in enumerate(responses):
                result["per_request"].append({
                    "request_id": f"conc{conc}-req{i+1:03d}",
                    "prompt_length": len(batch_prompts[i]),
                    "ttft_ms": round(r.ttft_ms, 2),
                    "tpot_ms": round(r.tpot_ms, 2),
                    "total_tokens": r.completion_tokens,
                    "gpu_memory_mb": max(gpu_mem) if gpu_mem else 0,
                    "gpu_utilization_pct": round(sum(gpu_util) / len(gpu_util), 1) if gpu_util else 0.0,
                    "error": None if r.text.strip() else "Empty response",
                })
            
            print(f"  TTFT p50: {result['results'][f'concurrency_{conc}']['ttft_p50_ms']} ms")
            print(f"  TPOT p50: {result['results'][f'concurrency_{conc}']['tpot_p50_ms']} ms")
            print(f"  Throughput: {result['results'][f'concurrency_{conc}']['throughput_tokens_per_sec']} tok/s")
            print(f"  GPU util: {result['results'][f'concurrency_{conc}']['gpu_utilization_mean_pct']}%")
        
        result["ops_notes"]["status"] = "PASS"
        print(f"\n=== LLMPerf {engine.upper()}: PASS ===")
        
    except Exception as e:
        result["ops_notes"]["status"] = f"FAIL: {e}"
        print(f"\n=== LLMPerf {engine.upper()}: FAIL ===")
        print(f"  Error: {e}")
    finally:
        adapter.teardown()
    
    # Save result
    out_dir = os.path.join(os.path.dirname(__file__), "benchmarks")
    os.makedirs(out_dir, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = os.path.join(out_dir, f"llmperf-{engine}-{date_str}.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"  Result saved: {out_path}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLMPerf benchmark runner")
    parser.add_argument("--engine", required=True, choices=list(ENGINE_MAP.keys()))
    parser.add_argument("--model", required=True)
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--concurrency", default="1,2,4,8,16", help="Comma-separated concurrency levels")
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--timeout", type=float, default=300.0)
    args = parser.parse_args()
    
    conc_levels = [int(x.strip()) for x in args.concurrency.split(",")]
    run_llmperf(
        engine=args.engine,
        model=args.model,
        gpu=args.gpu,
        concurrency_levels=conc_levels,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        port=args.port,
        timeout=args.timeout,
    )
