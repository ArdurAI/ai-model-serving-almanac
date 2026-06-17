"""
ModelServingAdapter — frozen contract for all inference-engine benchmarks.

Every engine on the roster must satisfy this interface to enter the standard
benchmark pipeline. The adapter is the only per-engine code that changes;
the harness, prompts, judge, and scoring rubric are fixed.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
import time


@dataclass
class Response:
    """Standardized response from any serving engine."""
    text: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    ttft_ms: float = 0.0          # Time-to-first-token (wall-clock)
    tpot_ms: float = 0.0          # Time-per-output-token (average)
    finish_reason: str = "stop"
    raw_response: Any = None       # Engine-specific payload (for debugging)


@dataclass
class Telemetry:
    """GPU / system telemetry snapshot."""
    timestamp: float
    gpu_memory_used_mb: List[float] = field(default_factory=list)
    gpu_memory_total_mb: List[float] = field(default_factory=list)
    gpu_utilization_pct: List[float] = field(default_factory=list)
    gpu_temperature_c: List[float] = field(default_factory=list)
    cpu_percent: Optional[float] = None
    ram_used_mb: Optional[float] = None
    ram_total_mb: Optional[float] = None


class ModelServingAdapter(ABC):
    """
    Frozen adapter contract. Do NOT modify the interface without an RFC
    and a public announcement (see TESTING.md § Methodology changes).
    """

    def __init__(self, engine_name: str, model_id: str, gpu_devices: List[int] = None):
        self.engine_name = engine_name
        self.model_id = model_id
        self.gpu_devices = gpu_devices or [0]
        self._server_proc = None   # subprocess.Popen or similar
        self._base_url = None      # e.g. "http://localhost:8000"

    # ── Lifecycle ────────────────────────────────────────────────────────────

    @abstractmethod
    def setup(self) -> None:
        """
        Install, configure, and start the serving engine.
        Must set `self._base_url` and populate `self._server_proc` if a
        subprocess is launched.
        """
        pass

    @abstractmethod
    def load(self, model_path: str, quantization: Optional[str] = None) -> None:
        """
        Load the model weights into the engine.
        For engines that bake this into `setup()` (e.g. Docker images with
        embedded weights) this may be a no-op.
        """
        pass

    @abstractmethod
    def await_ready(self, timeout: float = 300.0) -> None:
        """
        Wait for the engine to report ready (health check passes).
        Then send a warm-up request to ensure JIT compilation / graph capture
        overhead is NOT hidden in the first benchmark request.

        Raises TimeoutError if `timeout` seconds elapse without health.
        """
        pass

    @abstractmethod
    def query(self, prompt: str, max_tokens: int, temperature: float = 0.0) -> Response:
        """
        Send a single completion request and return the standardized Response.
        Must measure TTFT from the moment the HTTP request is sent until the
        first response token is received.
        """
        pass

    @abstractmethod
    def batch_query(self, prompts: List[str], max_tokens: int,
                    temperature: float = 0.0) -> List[Response]:
        """
        Send concurrent requests and return responses.
        The harness controls concurrency level; the adapter should use
        asyncio, concurrent.futures, or threaded workers to parallelize.
        """
        pass

    @abstractmethod
    def teardown(self) -> None:
        """
        Clean up: stop the server, release GPU memory, kill zombie processes.
        After teardown, `nvidia-smi` should show no remaining processes
        from this engine.
        """
        pass

    @abstractmethod
    def get_telemetry(self) -> Telemetry:
        """
        Return a Telemetry snapshot. Should call `nvidia-smi` or `pynvml`
        to read GPU state.
        """
        pass

    # ── Optional hooks ───────────────────────────────────────────────────────

    def pre_benchmark(self) -> None:
        """Called once before the first benchmark request."""
        pass

    def post_benchmark(self) -> None:
        """Called once after the last benchmark request."""
        pass

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.teardown()
        return False

    # ── Utilities ────────────────────────────────────────────────────────────

    def _poll_health(self, url: str, timeout: float) -> None:
        """Generic HTTP health polling used by many adapters."""
        import requests
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                r = requests.get(url, timeout=5.0)
                if r.status_code == 200:
                    return
            except Exception:
                pass
            time.sleep(1.0)
        raise TimeoutError(f"Health check failed at {url} after {timeout}s")

    def _warmup(self, prompt: str = "Hello world", max_tokens: int = 8) -> None:
        """Send a trivial warm-up request to trigger JIT / graph capture."""
        self.query(prompt, max_tokens, temperature=0.0)

    def _nvml_telemetry(self) -> Telemetry:
        """Read GPU telemetry via pynvml."""
        try:
            import pynvml
            pynvml.nvmlInit()
            n_gpu = pynvml.nvmlDeviceGetCount()
            t = Telemetry(timestamp=time.time())
            for i in range(n_gpu):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                t.gpu_memory_used_mb.append(mem.used / 1024 / 1024)
                t.gpu_memory_total_mb.append(mem.total / 1024 / 1024)
                t.gpu_utilization_pct.append(util.gpu)
                try:
                    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                    t.gpu_temperature_c.append(temp)
                except Exception:
                    t.gpu_temperature_c.append(0.0)
            return t
        except Exception as e:
            # Fallback: return empty telemetry with error note
            return Telemetry(timestamp=time.time(), gpu_utilization_pct=[-1.0])
