from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent.parent.parent / ".env"),
        case_sensitive=False,
    )

    # API Keys
    anthropic_api_key: str = ""

    # Application
    debug: bool = True
    log_level: str = "INFO"

    # Paths
    raw_data_dir: str = "data/raw"
    wiki_dir: str = "data/wiki"
    output_dir: str = "data/output"

    # LLM
    model: str = "claude-haiku-4-5-20251001"
    max_tokens: int = 4096
    temperature: float = 0.7

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_port: int = 5173
    
    @property
    def raw_data_path(self) -> Path:
        # Resolve relative to project root, not current working directory
        project_root = Path(__file__).parent.parent.parent
        return project_root / self.raw_data_dir

    @property
    def wiki_path(self) -> Path:
        # Resolve relative to project root, not current working directory
        project_root = Path(__file__).parent.parent.parent
        return project_root / self.wiki_dir

    @property
    def output_path(self) -> Path:
        # Resolve relative to project root, not current working directory
        project_root = Path(__file__).parent.parent.parent
        return project_root / self.output_dir


settings = Settings()
