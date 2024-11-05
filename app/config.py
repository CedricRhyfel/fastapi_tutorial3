from pydantic_settings import BaseSettings, SettingsConfigDict

# load_dotenv()
# config = dotenv_values(".env")
# print(dict(config))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='./app/.env', env_file_encoding='utf-8')

    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

settings = Settings()
