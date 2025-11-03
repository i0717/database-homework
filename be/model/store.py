import logging
import os
import pymongo
from pymongo import MongoClient
import threading


class Store:
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
    global database_instance
    database_instance = Store(db_path)


def get_db():
    global database_instance
    return database_instance.get_db()