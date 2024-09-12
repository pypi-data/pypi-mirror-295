from typing import TypeAlias

from mm_mongo import MongoCollection
from pymongo.database import Database

from mm_base1.models import DConfig, DLog, DValue

DatabaseAny: TypeAlias = Database[dict[str, object]]


class BaseDB:
    def __init__(self, database: DatabaseAny) -> None:
        self.dconfig: MongoCollection[DConfig] = DConfig.init_collection(database)
        self.dvalue: MongoCollection[DValue] = DValue.init_collection(database)
        self.dlog: MongoCollection[DLog] = DLog.init_collection(database)
