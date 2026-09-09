"""Run the extracted suite without silently accepting missing dependencies."""

from pathlib import Path
import sys
import unittest


def main():
    try:
        import numpy
        import PIL
    except ImportError as exc:
        print(f"Missing dependency: {exc}. Install MRI/requirements.txt.", file=sys.stderr)
        return 2
    print(f"Python {sys.version.split()[0]}; NumPy {numpy.__version__}; Pillow {PIL.__version__}",
          flush=True)
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parent),
                                               pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.skipped:
        print("Incomplete verification: skipped tests are not accepted.", file=sys.stderr)
    return 0 if result.wasSuccessful() and result.testsRun > 0 and not result.skipped else 1


if __name__ == "__main__":
    raise SystemExit(main())
