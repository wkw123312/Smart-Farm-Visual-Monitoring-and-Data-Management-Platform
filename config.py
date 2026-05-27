import os
from pathlib import Path
from typing import Any, Optional

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_CONFIG = {
    "project_root": "./",
    "dataset_root": "./BCCD",
    "data_yaml": "./datasets/data.yaml",
    "model_path": "./yolov8n.pt",
    "output_dir": "./runs",
    "log_dir": "./logs",
    "device": "cpu",
    "gradio_port": 7861,
    "secret_key": "replace-with-your-secret-key",
    "debug": True,
    "allowed_hosts": ["localhost", "127.0.0.1"],
}


def load_config(config_path: Optional[str] = None) -> dict[str, Any]:
    config_path = config_path or os.getenv("CONFIG_PATH", "config.yaml")
    path = Path(config_path)
    if not path.exists():
        return DEFAULT_CONFIG.copy()

    if yaml is None:
        raise ImportError(
            "PyYAML is required to load config.yaml. Install with `pip install pyyaml`."
        )

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError("Config file must contain a YAML mapping.")

    config = DEFAULT_CONFIG.copy()
    config.update({k: v for k, v in data.items() if v is not None})
    return config


if __name__ == "__main__":
    import json

    cfg = load_config()
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
