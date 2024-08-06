from pathlib import Path
from typing import Optional, IO

import dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_api_key: SecretStr
    llm_endpoint: str

    llm_type: str = "azure"
    llm_version: str = "2024-02-01"
    llm_deployment_name: str = "gpt-4o"

    llm_request_timeout: float = 180.0
    llm_max_retries: int = 30

    llm_temperature: Optional[float] = 0
    llm_top_p: Optional[float] = None
    llm_seed: Optional[int] = 42
    llm_presence_penalty: Optional[float] = None
    llm_frequency_penalty: Optional[float] = None
    llm_logit_bias: Optional[dict[str, int]] = None

    llm_log_level: str = "INFO"


def load_env_settings(
        dotenv_path: Optional[Path] = None,
        dotenv_stream: Optional[IO[str]] = None,
) -> Settings:
    success = dotenv.load_dotenv(
        dotenv_path=dotenv_path,
        stream=dotenv_stream,
        verbose=True,
    )
    if not success:
        raise ValueError("Failed to load .env file")
    return Settings()  # pyright: ignore [reportCallIssue]
