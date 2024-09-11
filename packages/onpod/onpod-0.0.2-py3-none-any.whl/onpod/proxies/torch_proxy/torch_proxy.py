'''
This module provides a proxy for PyTorch operations, automatically managing
remote execution on a RunPod instance. It initializes with a CPU-based
instance for efficient resource usage and dynamically claims a GPU when
models are moved to CUDA devices. This approach optimizes cloud resource
utilization while providing seamless access to GPU acceleration when needed.

The proxy intercepts PyTorch operations, redirecting them to the remote
instance, and handles the necessary data transfer and execution management.
This allows users to write standard PyTorch code locally, while benefiting
from the computational power of cloud-based resources without manual
configuration.


todo
- torch.distributed automatically configure multiple gpus for distributed training / inference

'''

import typing
import torch

def __getattr__(name: str):
    print("__getattr__", name)
    return getattr(torch, name)


def __init__(self, *args, **kwargs):
    print("__init__", args, kwargs)
    super().__init__(*args, **kwargs)