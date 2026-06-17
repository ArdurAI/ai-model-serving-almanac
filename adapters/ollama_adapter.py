"""
OllamaAdapter — concrete adapter for the Ollama local LLM serving tool.

Ollama is NOT production-ready for multi-tenant serving, but it is a Tier A
entry because of its massive adoption (52M+ monthly downloads) and ubiquity as
a local dev tool. This adapter tests it as a local inference engine, not as a
production serving platform.

Setup: launches `ollama serve` as a subprocess (or connects to an already-
running server), then queries the native Ollama REST API.
"""

import subprocess, time, signal, os, requests, json
from typing import List, Optional
from adapters import ModelServingAdapter, Response, Telemetry


class OllamaAdapter(ModelServingAdapter):
    """
    Ollama adapter. Uses the native Ollama API (not OpenAI-compatible).
    Endpoint: http://localhost:11434/api/chat
    """

    def __init__(self, model_id: str, gpu_devices: List[int] = None,
                 port: int = 11434, host: str = "0.0.0.0"):
        self.port = port
        self.host = host
        super().__init__("ollama", model_id, gpu_devices)
        self._base_url = f"http://localhost:{port}"

    def setup(self) -> None:
        """Launch `ollama serve` if not already running."""
        import psutil
        already_running = False
        for p in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if "ollama" in " ".join(p.info["cmdline"] or []):
                    already_running = True
                    self._server_proc = None
                    break
            except Exception:
                pass
        if not already_running:
            env = os.environ.copy()
            if self.gpu_devices:
                env["CUDA_VISIBLE_DEVICES"] = ",".join(str(d) for d in self.gpu_devices)
            self._server_proc = subprocess.Popen(
                ["ollama", "serve"],
                env=env,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            print(f"[Ollama] Started PID {self._server_proc.pid}")
        else:
            print("[Ollama] Server already running; reusing.")

    def load(self, model_path: str, quantization: Optional[str] = None) -> None:
        """Pull the model via `ollama pull`."""
        subprocess.run(["ollama", "pull", self.model_id], check=True)
        print(f"[Ollama] Pulled {self.model_id}")

    def await_ready(self, timeout: float = 300.0) -> None:
        """Poll the Ollama tags endpoint as a health check."""
        self._poll_health(f"{self._base_url}/api/tags", timeout)
        self._warmup()
        print(f"[Ollama] Ready on {self._base_url}")

    def query(self, prompt: str, max_tokens: int, temperature: float = 0.0) -> Response:
        t0 = time.perf_counter()
        r = requests.post(
            f"{self._base_url}/api/chat",
            json={
                "model": self.model_id,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": temperature, "num_predict": max_tokens},
            },
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        t_total = time.perf_counter() - t0
        message = data.get("message", {})
        text = message.get("content", "")
        # Ollama does not stream by default in this endpoint; TTFT ≈ total time
        return Response(
            text=text,
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            ttft_ms=t_total * 1000.0,
            tpot_ms=0.0,
            raw_response=data,
        )

    def batch_query(self, prompts: List[str], max_tokens: int,
                    temperature: float = 0.0) -> List[Response]:
        from concurrent.futures import ThreadPoolExecutor
        def _one(p: str) -> Response:
            return self.query(p, max_tokens, temperature)
        # Ollama default concurrency is 1; parallel requests will queue
        with ThreadPoolExecutor(max_workers=len(prompts)) as ex:
            return list(ex.map(_one, prompts))

    def teardown(self) -> None:
        if self._server_proc is not None:
            self._server_proc.send_signal(signal.SIGTERM)
            try:
                self._server_proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self._server_proc.kill()
                self._server_proc.wait(timeout=10)
            print(f"[Ollama] Terminated PID {self._server_proc.pid}")

    def get_telemetry(self) -> Telemetry:
        return self._nvml_telemetry()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Ollama smoke gate")
    parser.add_argument("--model", default="gemma4")
    parser.add_argument("--port", type=int, default=11434)
    parser.add_argument("--gpu", type=int, default=0)
    args = parser.parse_args()

    print(f"=== Ollama Smoke Gate: {args.model} ===")
    adapter = OllamaAdapter(args.model, gpu_devices=[args.gpu], port=args.port)
    adapter.setup()
    try:
        adapter.await_ready(timeout=60.0)
        resp = adapter.query("Hello, what is 2+2?", max_tokens=32, temperature=0.0)
        print(f"Response: {resp.text}")
        print(f"TTFT: {resp.ttft_ms:.1f} ms")
        assert resp.text.strip(), "Empty response"
        print("PASS")
    finally:
        adapter.teardown()
