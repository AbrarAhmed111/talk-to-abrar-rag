"""LLM RAG Starter Application Package."""

import sys
from pathlib import Path

# Compatibility alias so both `src.app.*` and `app.*` imports resolve to the same package.
# This keeps the current project working with the existing tests and runtime code.
if "app" not in sys.modules:
    sys.modules["app"] = sys.modules[__name__]

__path__ = [str(Path(__file__).resolve().parent)]
