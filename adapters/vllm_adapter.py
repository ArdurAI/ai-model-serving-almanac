"""
VLLMAdapter — concrete adapter for the vLLM inference engine.

Runs `vllm serve` as a subprocess, then queries via the OpenAI-compatible
REST API. This is a production-ready adapter pattern that other LLMPerfAdapter
engines can copy with minimal changes.
"""

import subprocess, time, signal, os, requests
from typing import List, Optional
from adapters.llmperf_adapter import LLMPerfAdapter
from adapters import Response, Telemetry


class VLLMAdapter(LLMPerfAdapter):
    """
    vLLM adapter: launches `vllm serve` locally, waits for health,
    then benchmarks via the OpenAI-compatible endpoint.
    """

    def __init__(self, model_id: str, gpu_devices: List[int] = None,
                 port: int = 8000, quantization: Optional[str] = None,
                 extra_args: List[str] = None):
        self.port = port
        self.quantization = quantization
        self.extra_args = extra_args or []
        base_url = f"http://localhost:{port}"
        # vLLM does not require an API key for local serving
        super().__init__("vllm", model_id, base_url, api_key="dummy",
                         gpu_devices=gpu_devices)

    def setup(self) -> None:
        """Launch `vllm serve` in a subprocess."""
        cmd = [
            "vllm", "serve", self.model_id,
            "--port", str(self.port),
            "--host", "0.0.0.0",
        ]
        if self.quantization:
            cmd += ["--quantization", self.quantization]
        if self.gpu_devices:
            os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str(d) for d in self.gpu_devices)
        cmd += self.extra_args

        self._server_proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(f"[vLLM] Started PID {self._server_proc.pid} on port {self.port}")

    def await_ready(self, timeout: float = 300.0) -> None:
        """Poll /health, then send a warm-up request."""
        health_url = f"{self.base_url}/health"
        self._poll_health(health_url, timeout)
        self._warmup()
        print(f"[vLLM] Ready and warmed up on {self.base_url}")

    def teardown(self) -> None:
        """Graceful shutdown of vLLM server."""
        if self._server_proc is not None:
            self._server_proc.send_signal(signal.SIGTERM)
            try:
                self._server_proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self._server_proc.kill()
                self._server_proc.wait(timeout=10)
            print(f"[vLLM] Terminated PID {self._server_proc.pid}")
        # vLLM sometimes leaves zombie CUDA processes; force cleanup
        import psutil
        for p in psutil.process_iter(["pid", "name"]):
            try:
                if p.info["name"] in ("python", "python3"):
                    cmdline = " ".join(p.cmdline())
                    if "vllm" in cmdline and p.pid != os.getpid():
                        p.terminate()
                        p.wait(timeout=5)
            except Exception:
                pass

    def get_telemetry(self) -> Telemetry:
        return self._nvml_telemetry()


# ── Stand-alone smoke gate ─────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="vLLM smoke gate")
    parser.add_argument("--model", default="meta-llama/Meta-Llama-3.1-8B-Instruct")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--gpu", type=int, default=0)
    args = parser.parse_args()

    print(f"=== vLLM Smoke Gate: {args.model} ===")
    adapter = VLLMAdapter(args.model, gpu_devices=[args.gpu], port=args.port)
    adapter.setup()
    try:
        adapter.await_ready(timeout=120.0)
        resp = adapter.query("Hello, what is 2+2?", max_tokens=32, temperature=0.0)
        print(f"Response: {resp.text}")
        print(f"TTFT: {resp.ttft_ms:.1f} ms")
        print(f"Tokens: {resp.completion_tokens}")
        assert resp.text.strip(), "Empty response"
        print("PASS")
    finally:
        adapter.teardown()
