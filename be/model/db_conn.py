from be.model import store


class DBConn:
    def __init__(self):
<<<<<<< HEAD
        self.db = store.get_db()

    def user_id_exist(self, user_id):
        # 检查用户是否存在
        return self.db.user.find_one({'user_id': user_id}) is not None

    def book_id_exist(self, store_id, book_id):
        # 检查店铺中是否存在书籍
        return self.db.store.find_one({
            'store_id': store_id,
            'book_id': book_id
        }) is not None

    def store_id_exist(self, store_id):
        # 检查店铺是否存在
        return self.db.user_store.find_one({'store_id': store_id}) is not None
=======
        self.conn = store.get_db_conn()

    def user_id_exist(self, user_id):
        cursor = self.conn.execute(
            "SELECT user_id FROM user WHERE user_id = ?;", (user_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        cursor = self.conn.execute(
            "SELECT book_id FROM store WHERE store_id = ? AND book_id = ?;",
            (store_id, book_id),
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        cursor = self.conn.execute(
            "SELECT store_id FROM user_store WHERE store_id = ?;", (store_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
