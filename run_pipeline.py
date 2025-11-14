"""Run the data pipeline scripts in order.

This helper runs the main pipeline scripts to reproduce cleaned data, analyses and models.
It uses the same Python interpreter that's running this script.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SCRIPTS = [
    ROOT / 'scripts' / 'data_loading.py',
    ROOT / 'scripts' / 'exploratory_analysis.py',
    ROOT / 'scripts' / 'trend_analysis.py',
    ROOT / 'scripts' / 'predictions.py',
    ROOT / 'scripts' / 'final_insights.py',
]


def run_script(path: Path) -> int:
    print(f"Running: {path.name}")
    if not path.exists():
        print(f"Script not found: {path}")
        return 1
    res = subprocess.run([sys.executable, str(path)], cwd=ROOT)
    return res.returncode


def main():
    for s in SCRIPTS:
        code = run_script(s)
        if code != 0:
            print(f"Script failed: {s} (exit {code})")
            sys.exit(code)
    print("Pipeline completed successfully.")


if __name__ == '__main__':
    main()
