from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str | None = None):
    env = Env()
    if path:
        env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=env.list('ADMINS'),
            use_redis=env.bool('USE_REDIS'),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        )
    )
