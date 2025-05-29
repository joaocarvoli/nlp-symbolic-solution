from huggingface_hub import hf_hub_download
from my_lightning_module import MyModel

ckpt_path = hf_hub_download(
    repo_id='jvcarvoli/bertimbau-for-sentiment',
    filename='epoch=4-step=19930.ckpt'
)

print("Checkpoint is at:", ckpt_path)
model = MyModel.load_from_checkpoint(ckpt_path)
