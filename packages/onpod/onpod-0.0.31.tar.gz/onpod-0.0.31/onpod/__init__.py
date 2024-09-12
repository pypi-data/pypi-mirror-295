from onpod.models.settings import Settings
import onpod.proxies.torch_proxy.torch_proxy as torch
import onpod.proxies.transformers_proxy as transformers
import onpod.proxies.tensorflow_proxy as tensorflow

__all__ = ["torch", "transformers", "tensorflow"]

class OnPod:
    settings: Settings = Settings()

    def __init__(self):
        pass
    



