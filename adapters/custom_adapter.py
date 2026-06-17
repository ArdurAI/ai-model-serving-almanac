"""
CustomServingAdapter — for engines that do NOT expose an OpenAI-compatible API.

Engines: TensorRT-LLM (gRPC/LLM API), llama.cpp (native C API), NVIDIA Dynamo
(disaggregated, custom protocols), edge runtimes, etc.

The adapter must handle:
  - Custom request formatting (gRPC, custom HTTP, binary payloads)
  - Response parsing (non-JSON or binary)
  - Model format conversion (e.g. Safetensors -> TensorRT engine)
  - GPU readiness checks (NCCL, MIG, topology)
"""

import subprocess, time, os, json
from typing import List, Optional, Dict, Any
from adapters import ModelServingAdapter, Response, Telemetry


class CustomServingAdapter(ModelServingAdapter):
    """
    Base class for custom-protocol adapters. Subclass this and implement
    `setup()`, `query()`, and `batch_query()` for your engine's specific
    protocol.
    """

    def __init__(self, engine_name: str, model_id: str,
                 gpu_devices: List[int] = None, config: Dict[str, Any] = None):
        super().__init__(engine_name, model_id, gpu_devices)
        self.config = config or {}

    # ── Hooks that subclasses MUST override ──────────────────────────────────

    def setup(self) -> None:
        """Start the engine subprocess / container."""
        raise NotImplementedError

    def load(self, model_path: str, quantization: Optional[str] = None) -> None:
        """Convert model format if needed, then load."""
        raise NotImplementedError

    def query(self, prompt: str, max_tokens: int, temperature: float = 0.0) -> Response:
        raise NotImplementedError

    def batch_query(self, prompts: List[str], max_tokens: int,
                    temperature: float = 0.0) -> List[Response]:
        raise NotImplementedError

    def teardown(self) -> None:
        if self._server_proc is not None:
            self._server_proc.terminate()
            try:
                self._server_proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                self._server_proc.kill()
                self._server_proc.wait(timeout=10)
        self._kill_zombies()

    def get_telemetry(self) -> Telemetry:
        return self._nvml_telemetry()

    # ── Helpers for common custom-engine patterns ────────────────────────────

    def _run_subprocess(self, cmd: List[str], env: Optional[Dict[str, str]] = None,
                        cwd: Optional[str] = None) -> subprocess.Popen:
        """Launch a subprocess with CUDA_VISIBLE_DEVICES set."""
        merged_env = os.environ.copy()
        merged_env["CUDA_VISIBLE_DEVICES"] = ",".join(str(d) for d in self.gpu_devices)
        if env:
            merged_env.update(env)
        proc = subprocess.Popen(cmd, env=merged_env, cwd=cwd,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._server_proc = proc
        return proc

    def _kill_zombies(self) -> None:
        """Best-effort cleanup of engine-specific processes."""
        import psutil
        for p in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmd = " ".join(p.info["cmdline"] or [])
                if self.engine_name.lower() in cmd.lower():
                    p.terminate()
                    p.wait(timeout=5)
            except Exception:
                pass

    def _check_cuda(self) -> None:
        """Verify CUDA is available and the requested GPUs exist."""
        import torch
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA not available")
        n_gpu = torch.cuda.device_count()
        for d in self.gpu_devices:
            if d >= n_gpu:
                raise RuntimeError(f"GPU device {d} not found (only {n_gpu} GPUs)")
