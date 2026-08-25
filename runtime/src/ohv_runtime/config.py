from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ohv_env: str = "development"
    ohv_db_path: Path = Path("./data/ohv.db")
    ohv_artifact_dir: Path = Path("./data/artifacts")
    ohv_log_level: str = "INFO"
    ohv_shadow_mode: bool = True

    local_llm_base_url: str = "http://127.0.0.1:11434"
    local_llm_model: str = ""

    trendtrack_api_key: str = ""
    trendtrack_base_url: str = "https://api.trendtrack.io"

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    morning_brief_webhook_url: str = ""

    def ensure_dirs(self) -> None:
        self.ohv_db_path.parent.mkdir(parents=True, exist_ok=True)
        self.ohv_artifact_dir.mkdir(parents=True, exist_ok=True)
