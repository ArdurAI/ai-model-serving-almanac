"""
AnyScaleAdapter — sustained-throughput / goodput benchmark adapter.

Used for engines where we want sustained-load numbers (goodput, throughput,
error rate over time) rather than per-request latency micro-benchmarks.

Pattern: send requests at fixed concurrency for N seconds, measure:
  - goodput (successful requests / sec)
  - throughput (tokens / sec)
  - error rate
"""

import time
import asyncio
import aiohttp
from typing import List, Optional, Dict, Any
from adapters import ModelServingAdapter, Response, Telemetry


class AnyScaleAdapter(ModelServingAdapter):
    """
    Sustained-load benchmark adapter.
    Compatible with any engine that exposes an OpenAI-compatible endpoint.
    """

    def __init__(self, engine_name: str, model_id: str, base_url: str,
                 api_key: Optional[str] = None, gpu_devices: List[int] = None):
        super().__init__(engine_name, model_id, gpu_devices)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "dummy"

    def setup(self) -> None:
        pass

    def load(self, model_path: str, quantization: Optional[str] = None) -> None:
        pass

    def await_ready(self, timeout: float = 300.0) -> None:
        health_url = f"{self.base_url}/health"
        self._poll_health(health_url, timeout)

    def query(self, prompt: str, max_tokens: int, temperature: float = 0.0) -> Response:
        # Synchronous wrapper for single-request tests
        import requests
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        payload = {
            "model": self.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        t0 = time.perf_counter()
        r = requests.post(f"{self.base_url}/v1/chat/completions",
                        headers=headers, json=payload, timeout=120)
        t_total = time.perf_counter() - t0
        r.raise_for_status()
        data = r.json()
        choice = data["choices"][0]
        text = choice.get("message", {}).get("content", "")
        usage = data.get("usage", {})
        return Response(
            text=text,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            ttft_ms=t_total * 1000.0,   # Approximate: no streaming
            tpot_ms=0.0,
            raw_response=data,
        )

    def batch_query(self, prompts: List[str], max_tokens: int,
                    temperature: float = 0.0) -> List[Response]:
        # For burst concurrency tests
        from concurrent.futures import ThreadPoolExecutor
        def _one(p: str) -> Response:
            return self.query(p, max_tokens, temperature)
        with ThreadPoolExecutor(max_workers=len(prompts)) as ex:
            return list(ex.map(_one, prompts))

    # ── Sustained load (the AnyScale-specific addition) ────────────────────

    def run_sustained_load(self, prompts: List[str], duration_sec: int,
                           concurrency: int, max_tokens: int = 256,
                           temperature: float = 0.0) -> Dict[str, Any]:
        """
        Send requests at `concurrency` parallel workers for `duration_sec`
        seconds, cycling through `prompts`. Return aggregate metrics.
        """
        import asyncio, aiohttp, random, time
        import statistics

        url = f"{self.base_url}/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}

        results = {"success": 0, "error": 0, "ttft_ms": [], "total_tokens": 0,
                   "start_time": time.time(), "end_time": None}

        async def _worker(session: aiohttp.ClientSession, stop_event: asyncio.Event):
            while not stop_event.is_set():
                prompt = random.choice(prompts)
                payload = {
                    "model": self.model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
                t0 = time.perf_counter()
                try:
                    async with session.post(url, headers=headers, json=payload) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            ttft_ms = (time.perf_counter() - t0) * 1000.0
                            usage = data.get("usage", {})
                            results["success"] += 1
                            results["ttft_ms"].append(ttft_ms)
                            results["total_tokens"] += usage.get("total_tokens", 0)
                        else:
                            results["error"] += 1
                except Exception:
                    results["error"] += 1

        async def _main():
            timeout = aiohttp.ClientTimeout(total=120)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                stop = asyncio.Event()
                workers = [asyncio.create_task(_worker(session, stop))
                           for _ in range(concurrency)]
                await asyncio.sleep(duration_sec)
                stop.set()
                await asyncio.gather(*workers, return_exceptions=True)

        asyncio.run(_main())
        results["end_time"] = time.time()
        elapsed = results["end_time"] - results["start_time"]
        results["goodput_rps"] = results["success"] / elapsed
        results["throughput_tps"] = results["total_tokens"] / elapsed
        if results["ttft_ms"]:
            results["ttft_p50_ms"] = statistics.median(results["ttft_ms"])
            results["ttft_p95_ms"] = statistics.quantiles(results["ttft_ms"], n=20)[18] if len(results["ttft_ms"]) >= 20 else max(results["ttft_ms"])
        else:
            results["ttft_p50_ms"] = 0.0
            results["ttft_p95_ms"] = 0.0
        return results

    def teardown(self) -> None:
        pass

    def get_telemetry(self) -> Telemetry:
        return self._nvml_telemetry()
