"""
TensorRTLLMAdapter — concrete adapter for TensorRT-LLM.

TensorRT-LLM has two serving modes:
  1. Triton Inference Server with TensorRT-LLM backend (OpenAI-compatible via
     the Triton tensorrtllm_backend HTTP endpoint)
  2. Native Python LLM API (v1.0+, PyTorch-native, not HTTP)

This adapter uses mode 1: launches Triton Inference Server with the
TensorRT-LLM backend, then queries via the OpenAI-compatible endpoint.

Note: TensorRT-LLM requires an explicit engine build step (model weights ->
TensorRT engine). This adapter assumes the engine has already been built or
uses the PyTorch-native LLM API path (v1.0+) which skips the build.

For the benchmark pipeline, we use the Python LLM API path when possible to
avoid the engine build complexity, falling back to Triton if needed.
"""

import subprocess, time, signal, os, json
from typing import List, Optional, Dict, Any
from adapters import ModelServingAdapter, Response, Telemetry


class TensorRTLLMAdapter(ModelServingAdapter):
    """
    TensorRT-LLM adapter using the PyTorch-native LLM API (v1.0+).

    This is NOT HTTP-based; it uses the Python `tensorrt_llm.LLM` class
directly. For HTTP-based benchmarking, wrap this in a local FastAPI server
or use the Triton Inference Server adapter.
    """

    def __init__(self, model_id: str, gpu_devices: List[int] = None,
                 quantization: Optional[str] = None,
                 max_batch_size: int = 8, max_input_len: int = 4096,
                 max_seq_len: int = 8192):
        super().__init__("tensorrt-llm", model_id, gpu_devices)
        self.quantization = quantization
        self.max_batch_size = max_batch_size
        self.max_input_len = max_input_len
        self.max_seq_len = max_seq_len
        self._llm = None
        self._sampling_params = None

    def setup(self) -> None:
        # TensorRT-LLM setup is done in load() via the Python API
        pass

    def load(self, model_path: str, quantization: Optional[str] = None) -> None:
        try:
            from tensorrt_llm import LLM, SamplingParams
        except ImportError as e:
            raise RuntimeError(
                "tensorrt_llm not installed. Install with:\n"
                "  pip install tensorrt_llm -U --extra-index-url https://pypi.nvidia.com"
            ) from e

        q = quantization or self.quantization
        build_config = {
            "max_batch_size": self.max_batch_size,
            "max_input_len": self.max_input_len,
            "max_seq_len": self.max_seq_len,
        }
        if q:
            build_config["quantization"] = q

        # PyTorch-native API (v1.0+) — no explicit engine build needed
        self._llm = LLM(model=model_path)
        self._sampling_params = SamplingParams(temperature=0.0, max_tokens=32)
        print(f"[TensorRT-LLM] Loaded {model_path}")

    def await_ready(self, timeout: float = 300.0) -> None:
        if self._llm is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        # Warm-up generation
        list(self._llm.generate(["Hello world"], self._sampling_params))
        print("[TensorRT-LLM] Warmed up")

    def query(self, prompt: str, max_tokens: int, temperature: float = 0.0) -> Response:
        if self._llm is None:
            raise RuntimeError("Model not loaded.")

        from tensorrt_llm import SamplingParams
        sp = SamplingParams(temperature=temperature, max_tokens=max_tokens)

        t0 = time.perf_counter()
        outputs = list(self._llm.generate([prompt], sp))
        t_total = time.perf_counter() - t0

        text = outputs[0].text if outputs else ""
        # TensorRT-LLM doesn't expose token counts directly in the Python API
        return Response(
            text=text,
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            ttft_ms=t_total * 1000.0,  # Approximate (no streaming)
            tpot_ms=0.0,
            raw_response=None,
        )

    def batch_query(self, prompts: List[str], max_tokens: int,
                    temperature: float = 0.0) -> List[Response]:
        from tensorrt_llm import SamplingParams
        sp = SamplingParams(temperature=temperature, max_tokens=max_tokens)
        t0 = time.perf_counter()
        outputs = list(self._llm.generate(prompts, sp))
        t_total = time.perf_counter() - t0

        responses = []
        for i, out in enumerate(outputs):
            resp = Response(
                text=out.text,
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
                ttft_ms=(t_total / len(prompts)) * 1000.0,  # Approximate
                tpot_ms=0.0,
                raw_response=None,
            )
            responses.append(resp)
        return responses

    def teardown(self) -> None:
        if self._llm is not None:
            # TensorRT-LLM Python API doesn't have an explicit close,
            # but we can delete the reference and force GC
            del self._llm
            self._llm = None
            import gc
            gc.collect()
            import torch
            torch.cuda.empty_cache()
            print("[TensorRT-LLM] Cleaned up")

    def get_telemetry(self) -> Telemetry:
        return self._nvml_telemetry()


class TensorRTLLMTritonAdapter(ModelServingAdapter):
    """
    TensorRT-LLM adapter via Triton Inference Server.

    Requires:
      - Triton Inference Server Docker image or binary
      - TensorRT-LLM backend shared library
      - Pre-built TensorRT engine for the model
      - Model repository directory with config.pbtxt

    This is more complex than the Python API path and is typically used for
    production serving benchmarks.
    """

    def __init__(self, model_id: str, gpu_devices: List[int] = None,
                 port: int = 8000, model_repo: str = "./model_repo",
                 extra_args: List[str] = None):
        super().__init__("tensorrt-llm-triton", model_id, gpu_devices)
        self.port = port
        self.model_repo = model_repo
        self.extra_args = extra_args or []
        self._base_url = f"http://localhost:{port}"

    def setup(self) -> None:
        # Check for model repository
        if not os.path.exists(self.model_repo):
            raise FileNotFoundError(
                f"Triton model repository not found: {self.model_repo}\n"
                f"Build the TensorRT engine and create the model repository first.\n"
                f"See: https://nvidia.github.io/TensorRT-LLM/user-guide/deploy-triton.html"
            )

        cmd = [
            "tritonserver",
            "--model-repository", self.model_repo,
            "--http-port", str(self.port),
            "--allow-http", "1",
        ]
        if self.gpu_devices:
            os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str(d) for d in self.gpu_devices)
        cmd += self.extra_args

        self._server_proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        print(f"[TensorRT-LLM Triton] Started PID {self._server_proc.pid} on port {self.port}")

    def load(self, model_path: str, quantization: Optional[str] = None) -> None:
        # Triton loads models from the repository; this is a no-op
        pass

    def await_ready(self, timeout: float = 300.0) -> None:
        health_url = f"{self._base_url}/v2/health/ready"
        self._poll_health(health_url, timeout)
        # Warm-up via Triton HTTP API
        import requests
        headers = {"Content-Type": "application/json"}
        payload = {
            "text_input": "Hello world",
            "max_tokens": 8,
            "temperature": 0.0,
        }
        r = requests.post(
            f"{self._base_url}/v2/models/{self.model_id}/infer",
            headers=headers, json=payload, timeout=30
        )
        r.raise_for_status()
        print(f"[TensorRT-LLM Triton] Ready and warmed up")

    def query(self, prompt: str, max_tokens: int, temperature: float = 0.0) -> Response:
        import requests
        headers = {"Content-Type": "application/json"}
        payload = {
            "text_input": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        t0 = time.perf_counter()
        r = requests.post(
            f"{self._base_url}/v2/models/{self.model_id}/infer",
            headers=headers, json=payload, timeout=120
        )
        t_total = time.perf_counter() - t0
        r.raise_for_status()
        data = r.json()
        text = data.get("text_output", "")
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
        # Triton supports batch inference via the same endpoint with batch_size
        # For simplicity, we fall back to sequential requests
        return [self.query(p, max_tokens, temperature) for p in prompts]

    def teardown(self) -> None:
        if self._server_proc is not None:
            self._server_proc.send_signal(signal.SIGTERM)
            try:
                self._server_proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self._server_proc.kill()
                self._server_proc.wait(timeout=10)
            print(f"[TensorRT-LLM Triton] Terminated PID {self._server_proc.pid}")
        import psutil
        for p in psutil.process_iter(["pid", "name"]):
            try:
                if "tritonserver" in p.info["name"] or "tritonserver" in " ".join(p.cmdline()):
                    if p.pid != os.getpid():
                        p.terminate()
                        p.wait(timeout=5)
            except Exception:
                pass

    def get_telemetry(self) -> Telemetry:
        return self._nvml_telemetry()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TensorRT-LLM smoke gate")
    parser.add_argument("--model", required=True)
    parser.add_argument("--mode", default="python", choices=["python", "triton"])
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--model-repo", default="./model_repo")
    args = parser.parse_args()

    print(f"=== TensorRT-LLM Smoke Gate: {args.model} ({args.mode}) ===")
    if args.mode == "python":
        adapter = TensorRTLLMAdapter(args.model, gpu_devices=[args.gpu])
    else:
        adapter = TensorRTLLMTritonAdapter(
            args.model, gpu_devices=[args.gpu], port=args.port, model_repo=args.model_repo
        )

    adapter.setup()
    try:
        adapter.load(args.model)
        adapter.await_ready(timeout=120.0)
        resp = adapter.query("Hello, what is 2+2?", max_tokens=32, temperature=0.0)
        print(f"Response: {resp.text}")
        print(f"TTFT: {resp.ttft_ms:.1f} ms")
        assert resp.text.strip(), "Empty response"
        print("PASS")
    finally:
        adapter.teardown()
