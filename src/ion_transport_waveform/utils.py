from pathlib import Path

def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def ensure_dir(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
