from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 8000
    db_url: AnyUrl
    username: str
    password: str
    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_sec: int

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


settings = Settings()
