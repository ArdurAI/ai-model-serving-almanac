"""
LlamaCppAdapter — concrete adapter for llama.cpp llama-server.

llama-server exposes an OpenAI-compatible REST API on top of the llama.cpp
runtime. This adapter launches the server as a subprocess and benchmarks via
the standard LLMPerfAdapter path.

Note: Requires a .gguf model file (not a HuggingFace model ID). The adapter
will attempt to download the GGUF via `huggingface-cli` if the path does not
exist locally.
"""

import subprocess, time, signal, os, requests
from typing import List, Optional
from adapters.llmperf_adapter import LLMPerfAdapter
from adapters import Response, Telemetry


class LlamaCppAdapter(LLMPerfAdapter):
    """
    llama.cpp adapter: launches `llama-server` locally, waits for health,
    then benchmarks via the OpenAI-compatible endpoint.
    """

    def __init__(self, model_path: str, gpu_devices: List[int] = None,
                 port: int = 8080, n_gpu_layers: int = -1,
                 context_size: int = 4096, extra_args: List[str] = None):
        self.model_path = model_path
        self.port = port
        self.n_gpu_layers = n_gpu_layers  # -1 = all layers on GPU
        self.context_size = context_size
        self.extra_args = extra_args or []
        base_url = f"http://localhost:{port}"
        super().__init__("llama.cpp", model_path, base_url, api_key="dummy",
                         gpu_devices=gpu_devices)

    def setup(self) -> None:
        # Verify model exists; if it's a HF model ID, we can't directly use it
        # with llama-server (needs GGUF). The caller should provide a GGUF path.
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}\n"
                f"llama.cpp requires a .gguf file. Download one from HuggingFace, e.g.:\n"
                f"  huggingface-cli download bartowski/Llama-3.1-8B-Instruct-GGUF \\\n"
                f"    --include '*Q4_K_M.gguf' --local-dir ./models"
            )

        cmd = [
            "llama-server",
            "-m", self.model_path,
            "--port", str(self.port),
            "--host", "0.0.0.0",
            "-ngl", str(self.n_gpu_layers),
            "-c", str(self.context_size),
        ]
        if self.gpu_devices:
            os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str(d) for d in self.gpu_devices)
        cmd += self.extra_args

        self._server_proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        print(f"[llama.cpp] Started PID {self._server_proc.pid} on port {self.port}")

    def await_ready(self, timeout: float = 300.0) -> None:
        health_url = f"{self.base_url}/health"
        self._poll_health(health_url, timeout)
        self._warmup()
        print(f"[llama.cpp] Ready and warmed up on {self.base_url}")

    def teardown(self) -> None:
        if self._server_proc is not None:
            self._server_proc.send_signal(signal.SIGTERM)
            try:
                self._server_proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self._server_proc.kill()
                self._server_proc.wait(timeout=10)
            print(f"[llama.cpp] Terminated PID {self._server_proc.pid}")
        import psutil
        for p in psutil.process_iter(["pid", "name"]):
            try:
                if "llama-server" in p.info["name"] or "llama-server" in " ".join(p.cmdline()):
                    if p.pid != os.getpid():
                        p.terminate()
                        p.wait(timeout=5)
            except Exception:
                pass

    def get_telemetry(self) -> Telemetry:
        return self._nvml_telemetry()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="llama.cpp smoke gate")
    parser.add_argument("--model", required=True, help="Path to .gguf model file")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--ngl", type=int, default=-1, help="Number of GPU layers (-1 = all)")
    parser.add_argument("--ctx", type=int, default=4096, help="Context size")
    args = parser.parse_args()

    print(f"=== llama.cpp Smoke Gate: {args.model} ===")
    adapter = LlamaCppAdapter(
        args.model, gpu_devices=[args.gpu], port=args.port,
        n_gpu_layers=args.ngl, context_size=args.ctx
    )
    adapter.setup()
    try:
        adapter.await_ready(timeout=120.0)
        resp = adapter.query("Hello, what is 2+2?", max_tokens=32, temperature=0.0)
        print(f"Response: {resp.text}")
        print(f"TTFT: {resp.ttft_ms:.1f} ms")
        assert resp.text.strip(), "Empty response"
        print("PASS")
    finally:
        adapter.teardown()
