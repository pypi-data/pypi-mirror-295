"""
This module is for getting mac specific cpu info
"""

import subprocess
from pathlib import Path

from .cpu import PhysicalProcessor


class SysctlCpuReader:
    """Class to read and store cpu information using the BSD sysctl utility

    See https://man.freebsd.org/cgi/man.cgi?sysctl(8) for sysctl info
    """

    def __init__(self) -> None:
        self.sysctl_path = Path("/usr/sbin/sysctl")

    def read(self, content: str | None = None) -> dict[int, PhysicalProcessor]:
        if not content:
            content = self._read_sysctl_key("machdep.cpu")
        return self._parse_machdep_cpu(content)

    def _read_sysctl_key(self, key: str) -> str:
        ret = subprocess.check_output([str(self.sysctl_path), key])
        return ret.decode("utf-8").strip()

    def _get_key_value(self, line: str) -> tuple:
        key, value = line.split(":")
        return key.strip(), value.strip()

    def _parse_machdep_cpu(self, content: str) -> dict[int, PhysicalProcessor]:
        ret = {}
        for line in content.splitlines():
            key, value = self._get_key_value(line)
            key_no_prefix = key[len("machdep.cpu.") :]
            ret[key_no_prefix] = value

        proc = PhysicalProcessor(0)
        if "brand_string" in ret:
            proc.model = ret["brand_string"]

        core_count = 1
        if "core_count" in ret:
            core_count = int(ret["core_count"])

        for idx in range(core_count):
            proc.add_core(idx)

        thread_count = 1
        if "thread_count" in ret:
            thread_count = int(ret["thread_count"])
        threads_per_core = int(thread_count / core_count)
        for core in proc.cores.values():
            for idx in range(threads_per_core):
                core.add_thread(idx)
        return {0: proc}
