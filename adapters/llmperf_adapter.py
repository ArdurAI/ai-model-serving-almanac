"""
LLMPerfAdapter — for engines that expose an OpenAI-compatible HTTP API.

Engines: vLLM, SGLang, TGI, llama.cpp (llama-server), LMDeploy, etc.
"""

import time
import requests
import openai
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from adapters import ModelServingAdapter, Response, Telemetry


class LLMPerfAdapter(ModelServingAdapter):
    """
    Adapter for engines that speak the OpenAI REST API.
    The harness uses this to send LLMPerf-style requests and measure
    TTFT / TPOT / throughput under controlled concurrency.
    """

    def __init__(self, engine_name: str, model_id: str, base_url: str,
                 api_key: Optional[str] = None, gpu_devices: List[int] = None):
        super().__init__(engine_name, model_id, gpu_devices)
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "dummy"
        self._client = openai.OpenAI(base_url=self.base_url, api_key=self.api_key)

    def setup(self) -> None:
        # For most OpenAI-compatible engines, the server is started externally
        # or via a concrete subclass (e.g. VLLMAdapter). This base class
        # assumes the endpoint is already reachable.
        pass

    def load(self, model_path: str, quantization: Optional[str] = None) -> None:
        # OpenAI-compatible servers typically load models at startup.
        pass

    def await_ready(self, timeout: float = 300.0) -> None:
        health_url = f"{self.base_url}/health"
        self._poll_health(health_url, timeout)
        self._warmup()

    def query(self, prompt: str, max_tokens: int, temperature: float = 0.0) -> Response:
        t0 = time.perf_counter()
        stream = self._client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )
        first_token = True
        tokens = 0
        text_parts = []
        t_first = 0.0
        for chunk in stream:
            if first_token:
                t_first = time.perf_counter() - t0
                first_token = False
            delta = chunk.choices[0].delta.content or ""
            text_parts.append(delta)
            tokens += 1
        t_total = time.perf_counter() - t0
        text = "".join(text_parts)
        tpot = (t_total - t_first) / max(tokens, 1) if tokens > 0 else 0.0
        return Response(
            text=text,
            prompt_tokens=0,      # adapter does not count prompt tokens
            completion_tokens=tokens,
            total_tokens=tokens,
            ttft_ms=t_first * 1000.0,
            tpot_ms=tpot * 1000.0,
            raw_response=None,
        )

    def batch_query(self, prompts: List[str], max_tokens: int,
                    temperature: float = 0.0) -> List[Response]:
        def _one(p: str) -> Response:
            return self.query(p, max_tokens, temperature)
        # LLMPerf-style concurrency via thread pool
        with ThreadPoolExecutor(max_workers=len(prompts)) as ex:
            return list(ex.map(_one, prompts))

    def teardown(self) -> None:
        # Base class does not own the server process.
        pass

    def get_telemetry(self) -> Telemetry:
        return self._nvml_telemetry()
