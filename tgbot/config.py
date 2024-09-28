from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    host: str
    port: int

    @property
    def db_url(self) -> str:
        raise NotImplementedError

    @property
    def db_url_async(self) -> str:
        raise NotImplementedError


@dataclass
class PgDbConfig(DbConfig):
    password: str
    user: str
    database: str

    @property
    def db_url(self) -> str:
        return (
            f'postgresql://{self.user}:{self.password}@'
            f'{self.host}:{self.port}/{self.database}'
        )

    @property
    def db_url_async(self) -> str:
        return f'postgresql+asyncpg://' + self.db_url.split('//')[-1]


@dataclass
class RedisDbConfig(DbConfig):
    password: str | None = None
    user: str | None = None
    database: str = '1'

    @property
    def db_url(self) -> str:
        url = 'redis://'
        if self.user is not None and self.password is not None:
            url += f'{self.user}:{self.password}@'
        url += f'f{self.host}:{self.port}/{self.database}'
        return url

    @property
    def db_url_async(self) -> str:
        return self.db_url


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
        db=PgDbConfig(
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        )
    )
