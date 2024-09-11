from pydantic.env_settings import BaseSettings


class RunPodSettings(BaseSettings):
    """
    Configuration for the RunPod API.
    """
    api_key: str
    api_url: str = "https://api.runpod.ai/v2"



class Settings(BaseSettings):
    """
    Configuration for the application.
    """
    runpod: RunPodSettings = RunPodSettings()
    


