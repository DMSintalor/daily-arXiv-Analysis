from util.functional import get_cfg
from .mysql import MySQLController
from .redis import RedisController


class DatabaseController(object):
    redis = None
    mysql = None

    def __init__(self, cfg=None):
        self.cfg = cfg if cfg else get_cfg()
        self.load_mysql()
        self.load_redis()

    def create_db(self):
        self.mysql.create_all()

    def load_mysql(self):
        self.mysql = MySQLController(**self.cfg['mysql'])

    def load_redis(self):
        self.redis = RedisController(**self.cfg['redis'])

    def get_base(self):
        return self.mysql.get_base()
