import json
import os


def write(
    dir,
    captions_config,
):
    os.makedirs(dir, exist_ok=True)

    captions_path = os.path.join(dir, "captions.json")
    with open(captions_path, "w") as f:
        f.write(json.dumps(captions_config, indent=2))
