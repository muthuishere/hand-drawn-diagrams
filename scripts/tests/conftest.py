"""Shared fixtures and path setup for the scripts test suite."""
from __future__ import annotations

import sys
from pathlib import Path

# Make the scripts directory importable from all test files
SCRIPTS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

TESTDATA = Path(__file__).parent / "testdata"
VALID_FILE = TESTDATA / "transportation-circulation-study-guide.excalidraw"
