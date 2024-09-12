from .models.settings import Settings
from runpod.api import ctl_commands
from runpod.cli.groups.config.functions import get_credentials

class Proxy:
    settings: Settings = Settings()

