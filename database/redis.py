import asyncio
import aioredis


class RedisController:
    def __init__(self, host='localhost', port=6379, password=None, db=0):
        self.host = host
        self.port = port
        self.password = password
        self.redis_db = db
        self.db = aioredis.from_url(
            'redis://{}:{}'.format(self.host, self.port),
            password=password,
            db=self.redis_db
        )

    async def set_value(self, key, value):
        await self.db.set(key, value)

    async def get_value(self, key):
        return await self.db.get(key)

    async def push_value(self, key, values):
        return await self.db.rpush(key, values)

    async def pop_value(self, key):
        return await self.db.lpop(key)


async def main(cfg):
    redis = RedisController(**cfg['redis'])
    await redis.set_value('test', 'hello')


if __name__ == '__main__':
    import yaml

    cfg = yaml.safe_load(open('../settings.yaml'))
    asyncio.run(main(cfg))
