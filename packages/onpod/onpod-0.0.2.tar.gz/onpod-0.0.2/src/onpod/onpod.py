from .models.settings import Settings
from runpod.api import ctl_commands
from runpod.cli.groups.config.functions import get_credentials

class OnPod:
    settings: Settings = Settings()


    def __init__(self):
        pass