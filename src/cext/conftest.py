"""
pytest configuration for C extension tests.
Adds build directory to sys.path before tests run.
"""

import sys
from pathlib import Path


def pytest_configure(config):
    """Add build directory to path before collecting tests."""
    test_dir = Path(__file__).parent
    build_dir = test_dir / "build"
    if build_dir.exists():
        sys.path.insert(0, str(build_dir))
