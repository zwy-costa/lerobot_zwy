from huggingface_hub import HfApi, snapshot_download
from lerobot.common.constants import HF_LEROBOT_HOME
import os

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

root = HF_LEROBOT_HOME / "weiye11"
root.mkdir(parents=True, exist_ok=True)

snapshot_download(
            "weiye11/act_0523_1020",
            # "weiye11/so100_423_pick",
            repo_type="dataset",
            # revision="v2.1",
            # revision="tutorial",
            local_dir=root,
            allow_patterns="meta/",
            ignore_patterns=None,
        )