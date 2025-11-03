from be.model import store


class DBConn:
    def __init__(self):
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