import logging
import time
import psutil
from pathlib import Path
from io import TextIOWrapper


logger = logging.getLogger(__name__)


class ResourceMonitor:

    def __init__(self, output_path: Path | None = None, stop_file: Path | None = None):
        self.target_proc = -1
        self.self_proc = -1
        self.sample_interval = 2000  # ms
        self.sample_duration = 0.0  # s

        self.output_path = output_path
        self.output_handle: TextIOWrapper | None = None

        self.stop_file = stop_file

    def sample(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        av_memory = memory.available / 1.0e6
        total_memory = memory.total / 1.0e6
        time_now = time.time()

        if self.output_handle:
            output = f"{time_now}, {cpu_percent}, {av_memory}, {total_memory}"
            self.output_handle.write(output + "\n")

    def before_sampling(self):
        psutil.cpu_percent(interval=None)
        if self.output_path:
            self.output_handle = open(self.output_path, "w", encoding="utf-8")

            self.output_handle.write(
                "Time (s), CPU (Percent), Memory Av (MB), Memory Total (MB)\n"
            )

    def run(self):
        count = 0
        self.before_sampling()
        while True:
            self.sample()
            time.sleep(self.sample_interval / 1000)
            count += 1
            if (
                self.sample_duration > 0
                and (self.sample_interval * count) / 1000 >= self.sample_duration
            ):
                break

            if self.stop_file and self.stop_file.exists():
                break

        if self.output_handle:
            self.output_handle.close()
