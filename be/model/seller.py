<<<<<<< HEAD
=======
import sqlite3 as sqlite
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
from be.model import error
from be.model import db_conn


class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

<<<<<<< HEAD
            self.db.store.insert_one({
                'store_id': store_id,
                'book_id': book_id,
                'book_info': book_json_str,
                'stock_level': stock_level
            })
            return 200, "ok"
        except Exception as e:
            return 528, f"{str(e)}"
=======
            self.conn.execute(
                "INSERT into store(store_id, book_id, book_info, stock_level)"
                "VALUES (?, ?, ?, ?)",
                (store_id, book_id, book_json_str, stock_level),
            )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc

    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

<<<<<<< HEAD
            result = self.db.store.update_one(
                {'store_id': store_id, 'book_id': book_id},
                {'$inc': {'stock_level': add_stock_level}}
            )
            if result.modified_count == 0:
                return 528, "更新库存失败"
            return 200, "ok"
        except Exception as e:
            return 528, f"{str(e)}"
=======
            self.conn.execute(
                "UPDATE store SET stock_level = stock_level + ? "
                "WHERE store_id = ? AND book_id = ?",
                (add_stock_level, store_id, book_id),
            )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)
<<<<<<< HEAD

            self.db.user_store.insert_one({
                'user_id': user_id,
                'store_id': store_id
            })
            return 200, "ok"
        except Exception as e:
            return 528, f"{str(e)}"
=======
            self.conn.execute(
                "INSERT into user_store(store_id, user_id)" "VALUES (?, ?)",
                (store_id, user_id),
            )
            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
