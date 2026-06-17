#!/usr/bin/env python3
"""
Sustained-Load Benchmark Runner — AnyScale-style sustained throughput test.

Sends requests at fixed concurrency for a sustained duration, measuring:
  - goodput (successful requests / sec)
  - throughput (tokens / sec)
  - error rate
  - TTFT p50/p95 under sustained load

Usage:
  python sustained_load_runner.py --engine vllm --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0 --concurrency 16 --duration 60
  python sustained_load_runner.py --engine sglang --model meta-llama/Meta-Llama-3.1-8B-Instruct --gpu 0 --concurrency 32 --duration 120

Produces a JSON result file in benchmarks/anyscale-<engine>-<date>.json.
"""

import argparse
import asyncio
import aiohttp
import json
import os
import random
import statistics
import time
from datetime import datetime, timezone
from typing import List, Dict, Any

from llmperf_runner import ENGINE_MAP, make_adapter, PROMPTS


def run_sustained_load(
    engine: str,
    model: str,
    gpu: int,
    concurrency: int,
    duration_sec: int,
    max_tokens: int = 256,
    temperature: float = 0.0,
    port: int = None,
    timeout: float = 300.0,
) -> Dict[str, Any]:
    """Run sustained-load benchmark."""
    
    adapter_kwargs = {"port": port} if port else {}
    adapter = make_adapter(engine, model, gpu, **adapter_kwargs)
    
    result = {
        "meta": {
            "benchmark_suite": "anyscale",
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
            "concurrency": concurrency,
            "duration_sec": duration_sec,
            "prompt_lengths": list(PROMPTS.keys()),
            "max_tokens": max_tokens,
            "temperature": temperature,
            "seed": 42,
        },
        "results": {},
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
        
        # Determine if the adapter supports async sustained load natively
        if hasattr(adapter, "run_sustained_load"):
            # AnyScaleAdapter has this method
            raw = adapter.run_sustained_load(
                list(PROMPTS.values()), duration_sec, concurrency, max_tokens, temperature
            )
            result["results"] = {
                "goodput_rps": round(raw.get("goodput_rps", 0.0), 2),
                "throughput_tps": round(raw.get("throughput_tps", 0.0), 2),
                "error_rate": round(raw.get("error", 0) / max(raw.get("success", 1) + raw.get("error", 0), 1), 4),
                "ttft_p50_ms": round(raw.get("ttft_p50_ms", 0.0), 2),
                "ttft_p95_ms": round(raw.get("ttft_p95_ms", 0.0), 2),
                "total_requests": raw.get("success", 0) + raw.get("error", 0),
                "successful_requests": raw.get("success", 0),
                "failed_requests": raw.get("error", 0),
                "duration_sec": duration_sec,
            }
        else:
            # Fallback: use synchronous batch_query in a loop with ThreadPoolExecutor
            from concurrent.futures import ThreadPoolExecutor
            import threading
            
            stop_event = threading.Event()
            metrics = {
                "success": 0, "error": 0, "ttft_ms": [], "total_tokens": 0,
            }
            lock = threading.Lock()
            
            prompts = list(PROMPTS.values())
            
            def _worker():
                while not stop_event.is_set():
                    prompt = random.choice(prompts)
                    try:
                        resp = adapter.query(prompt, max_tokens, temperature)
                        with lock:
                            metrics["success"] += 1
                            metrics["ttft_ms"].append(resp.ttft_ms)
                            metrics["total_tokens"] += resp.completion_tokens
                    except Exception:
                        with lock:
                            metrics["error"] += 1
            
            t_start = time.perf_counter()
            workers = []
            with ThreadPoolExecutor(max_workers=concurrency) as ex:
                for _ in range(concurrency):
                    workers.append(ex.submit(_worker))
                time.sleep(duration_sec)
                stop_event.set()
                for w in workers:
                    w.result(timeout=30)
            
            t_elapsed = time.perf_counter() - t_start
            total_reqs = metrics["success"] + metrics["error"]
            result["results"] = {
                "goodput_rps": round(metrics["success"] / t_elapsed, 2),
                "throughput_tps": round(metrics["total_tokens"] / t_elapsed, 2),
                "error_rate": round(metrics["error"] / max(total_reqs, 1), 4),
                "ttft_p50_ms": round(statistics.median(metrics["ttft_ms"]), 2) if metrics["ttft_ms"] else 0.0,
                "ttft_p95_ms": round(statistics.quantiles(metrics["ttft_ms"], n=20)[18], 2) if len(metrics["ttft_ms"]) >= 20 else (max(metrics["ttft_ms"]) if metrics["ttft_ms"] else 0.0),
                "total_requests": total_reqs,
                "successful_requests": metrics["success"],
                "failed_requests": metrics["error"],
                "duration_sec": duration_sec,
            }
        
        result["ops_notes"]["status"] = "PASS"
        print(f"\n=== Sustained Load {engine.upper()}: PASS ===")
        print(f"  Goodput: {result['results']['goodput_rps']} req/s")
        print(f"  Throughput: {result['results']['throughput_tps']} tok/s")
        print(f"  Error rate: {result['results']['error_rate']:.2%}")
        print(f"  TTFT p50: {result['results']['ttft_p50_ms']} ms")
        
    except Exception as e:
        result["ops_notes"]["status"] = f"FAIL: {e}"
        print(f"\n=== Sustained Load {engine.upper()}: FAIL ===")
        print(f"  Error: {e}")
    finally:
        adapter.teardown()
    
    # Save result
    out_dir = os.path.join(os.path.dirname(__file__), "benchmarks")
    os.makedirs(out_dir, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = os.path.join(out_dir, f"anyscale-{engine}-{date_str}.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"  Result saved: {out_path}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sustained-load benchmark runner")
    parser.add_argument("--engine", required=True, choices=list(ENGINE_MAP.keys()))
    parser.add_argument("--model", required=True)
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--concurrency", type=int, default=16)
    parser.add_argument("--duration", type=int, default=60, help="Duration in seconds")
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--timeout", type=float, default=300.0)
    args = parser.parse_args()
    
    run_sustained_load(
        engine=args.engine,
        model=args.model,
        gpu=args.gpu,
        concurrency=args.concurrency,
        duration_sec=args.duration,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        port=args.port,
        timeout=args.timeout,
    )
