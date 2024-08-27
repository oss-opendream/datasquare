import os

from huggingface_hub import login


login(token=os.getenv('DTSQR_HF_TOKEN'))
