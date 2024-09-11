# check if ckpt folder contains seq.ckpt and tokenizer.json
import warnings
from pathlib import Path

# Suppress the specific UserWarning based on the message
warnings.filterwarnings(
    "ignore",
    message="enable_nested_tensor is True, but self.use_nested_tensor is False because encoder_layer.norm_first was True"
)

ckpt = Path(__file__).parent / "ckpt"

if not ((ckpt / "seq.ckpt").exists() and (ckpt / "tokenizer.json").exists()):
    ckpt.mkdir(exist_ok=True)
    # Download the model checkpoint and tokenizer from the Hugging Face Hub
    from huggingface_hub import snapshot_download
    snapshot_download("wangyk22/CSTR", local_dir=ckpt, revision="main")