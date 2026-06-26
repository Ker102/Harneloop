from __future__ import annotations

import os
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


_THREAD_LOCKS: dict[Path, threading.RLock] = {}
_THREAD_LOCKS_GUARD = threading.Lock()


def harness_lock_path(harness_unit: Path, name: str) -> Path:
    safe_name = name.replace("\\", "__").replace("/", "__")
    return harness_unit / ".evolve" / "locks" / f"{safe_name}.lock"


def _thread_lock(path: Path) -> threading.RLock:
    resolved = path.resolve()
    with _THREAD_LOCKS_GUARD:
        lock = _THREAD_LOCKS.get(resolved)
        if lock is None:
            lock = threading.RLock()
            _THREAD_LOCKS[resolved] = lock
        return lock


@contextmanager
def file_lock(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    thread_lock = _thread_lock(path)
    with thread_lock:
        with path.open("a+b") as handle:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
                try:
                    yield
                finally:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
                try:
                    yield
                finally:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
