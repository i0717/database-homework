import logging
import os
<<<<<<< HEAD
import pymongo
from pymongo import MongoClient
=======
import sqlite3 as sqlite
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
import threading


class Store:
<<<<<<< HEAD
    def __init__(self, db_path=None):
        # 连接本地MongoDB，数据库名为bookstore
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['bookstore']
        self.init_collections()

    def init_collections(self):
        # 初始化集合（对应SQL表）
        try:
            # 用户表
            self.db.create_collection('user')
            self.db.user.create_index('user_id', unique=True)

            # 用户-店铺关联表
            self.db.create_collection('user_store')
            self.db.user_store.create_index([('user_id', 1), ('store_id', 1)], unique=True)

            # 店铺库存表
            self.db.create_collection('store')
            self.db.store.create_index([('store_id', 1), ('book_id', 1)], unique=True)

            # 订单表
            self.db.create_collection('new_order')
            self.db.new_order.create_index('order_id', unique=True)

            # 订单详情表
            self.db.create_collection('new_order_detail')
            self.db.new_order_detail.create_index([('order_id', 1), ('book_id', 1)], unique=True)

        except pymongo.errors.CollectionInvalid:
            # 集合已存在时忽略
            pass
        except Exception as e:
            logging.error(f"初始化集合失败: {e}")

    def get_db(self):
        return self.db


database_instance: Store = None
init_completed_event = threading.Event()


def init_database(db_path=None):
=======
    database: str

    def __init__(self, db_path):
        self.database = os.path.join(db_path, "be.db")
        self.init_tables()

    def init_tables(self):
        try:
            conn = self.get_db_conn()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS user ("
                "user_id TEXT PRIMARY KEY, password TEXT NOT NULL, "
                "balance INTEGER NOT NULL, token TEXT, terminal TEXT);"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS user_store("
                "user_id TEXT, store_id, PRIMARY KEY(user_id, store_id));"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "store_id TEXT, book_id TEXT, book_info TEXT, stock_level INTEGER,"
                " PRIMARY KEY(store_id, book_id))"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order( "
                "order_id TEXT PRIMARY KEY, user_id TEXT, store_id TEXT)"
            )

            conn.execute(
                "CREATE TABLE IF NOT EXISTS new_order_detail( "
                "order_id TEXT, book_id TEXT, count INTEGER, price INTEGER,  "
                "PRIMARY KEY(order_id, book_id))"
            )

            conn.commit()
        except sqlite.Error as e:
            logging.error(e)
            conn.rollback()

    def get_db_conn(self) -> sqlite.Connection:
        return sqlite.connect(self.database)


database_instance: Store = None
# global variable for database sync
init_completed_event = threading.Event()


def init_database(db_path):
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
    global database_instance
    database_instance = Store(db_path)


<<<<<<< HEAD
def get_db():
    global database_instance
    return database_instance.get_db()
=======
def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
