<<<<<<< HEAD
=======
import sqlite3 as sqlite
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
import uuid
import json
import logging
from be.model import db_conn
from be.model import error


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(
<<<<<<< HEAD
            self, user_id: str, store_id: str, id_and_count: [(str, int)]
=======
        self, user_id: str, store_id: str, id_and_count: [(str, int)]
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
    ) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
<<<<<<< HEAD

            order_id = f"{user_id}_{store_id}_{uuid.uuid1()}"

            # 检查并扣减库存
            for book_id, count in id_and_count:
                book = self.db.store.find_one({
                    'store_id': store_id,
                    'book_id': book_id
                })
                if not book:
                    return error.error_non_exist_book_id(book_id) + (order_id,)

                if book['stock_level'] < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                # 原子更新库存
                result = self.db.store.update_one(
                    {
                        'store_id': store_id,
                        'book_id': book_id,
                        'stock_level': {'$gte': count}
                    },
                    {'$inc': {'stock_level': -count}}
                )
                if result.modified_count == 0:
                    return error.error_stock_level_low(book_id) + (order_id,)

                # 添加订单详情
                book_info = json.loads(book['book_info'])
                self.db.new_order_detail.insert_one({
                    'order_id': order_id,
                    'book_id': book_id,
                    'count': count,
                    'price': book_info.get('price', 0)
                })

            # 创建订单
            self.db.new_order.insert_one({
                'order_id': order_id,
                'store_id': store_id,
                'user_id': user_id
            })
            return 200, "ok", order_id
        except Exception as e:
            logging.error(f"创建订单失败: {e}")
            return 528, f"{str(e)}", ""

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        try:
            # 查询订单
            order = self.db.new_order.find_one({'order_id': order_id})
            if not order:
                return error.error_invalid_order_id(order_id)

            buyer_id = order['user_id']
            store_id = order['store_id']
            if buyer_id != user_id:
                return error.error_authorization_fail()

            # 验证买家密码
            buyer = self.db.user.find_one({'user_id': buyer_id})
            if not buyer or buyer['password'] != password:
                return error.error_authorization_fail()

            # 查询卖家
            store = self.db.user_store.find_one({'store_id': store_id})
            if not store:
                return error.error_non_exist_store_id(store_id)
            seller_id = store['user_id']

            # 计算总金额
            details = self.db.new_order_detail.find({'order_id': order_id})
            total_price = sum(d['count'] * d['price'] for d in details)

            # 扣减买家余额
            if buyer['balance'] < total_price:
                return error.error_not_sufficient_funds(order_id)

            result = self.db.user.update_one(
                {'user_id': buyer_id, 'balance': {'$gte': total_price}},
                {'$inc': {'balance': -total_price}}
            )
            if result.modified_count == 0:
                return error.error_not_sufficient_funds(order_id)

            # 增加卖家余额
            result = self.db.user.update_one(
                {'user_id': seller_id},
                {'$inc': {'balance': total_price}}
            )
            if result.modified_count == 0:
                return error.error_non_exist_user_id(seller_id)

            # 删除订单及详情
            self.db.new_order.delete_one({'order_id': order_id})
            self.db.new_order_detail.delete_many({'order_id': order_id})

            return 200, "ok"
        except Exception as e:
            return 528, f"{str(e)}"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            user = self.db.user.find_one({'user_id': user_id})
            if not user or user['password'] != password:
                return error.error_authorization_fail()

            result = self.db.user.update_one(
                {'user_id': user_id},
                {'$inc': {'balance': add_value}}
            )
            if result.modified_count == 0:
                return error.error_non_exist_user_id(user_id)
            return 200, "ok"
        except Exception as e:
            return 528, f"{str(e)}"
=======
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            for book_id, count in id_and_count:
                cursor = self.conn.execute(
                    "SELECT book_id, stock_level, book_info FROM store "
                    "WHERE store_id = ? AND book_id = ?;",
                    (store_id, book_id),
                )
                row = cursor.fetchone()
                if row is None:
                    return error.error_non_exist_book_id(book_id) + (order_id,)

                stock_level = row[1]
                book_info = row[2]
                book_info_json = json.loads(book_info)
                price = book_info_json.get("price")

                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                cursor = self.conn.execute(
                    "UPDATE store set stock_level = stock_level - ? "
                    "WHERE store_id = ? and book_id = ? and stock_level >= ?; ",
                    (count, store_id, book_id, count),
                )
                if cursor.rowcount == 0:
                    return error.error_stock_level_low(book_id) + (order_id,)

                self.conn.execute(
                    "INSERT INTO new_order_detail(order_id, book_id, count, price) "
                    "VALUES(?, ?, ?, ?);",
                    (uid, book_id, count, price),
                )

            self.conn.execute(
                "INSERT INTO new_order(order_id, store_id, user_id) "
                "VALUES(?, ?, ?);",
                (uid, store_id, user_id),
            )
            self.conn.commit()
            order_id = uid
        except sqlite.Error as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        conn = self.conn
        try:
            cursor = conn.execute(
                "SELECT order_id, user_id, store_id FROM new_order WHERE order_id = ?",
                (order_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]

            if buyer_id != user_id:
                return error.error_authorization_fail()

            cursor = conn.execute(
                "SELECT balance, password FROM user WHERE user_id = ?;", (buyer_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_user_id(buyer_id)
            balance = row[0]
            if password != row[1]:
                return error.error_authorization_fail()

            cursor = conn.execute(
                "SELECT store_id, user_id FROM user_store WHERE store_id = ?;",
                (store_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return error.error_non_exist_store_id(store_id)

            seller_id = row[1]

            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            cursor = conn.execute(
                "SELECT book_id, count, price FROM new_order_detail WHERE order_id = ?;",
                (order_id,),
            )
            total_price = 0
            for row in cursor:
                count = row[1]
                price = row[2]
                total_price = total_price + price * count

            if balance < total_price:
                return error.error_not_sufficient_funds(order_id)

            cursor = conn.execute(
                "UPDATE user set balance = balance - ?"
                "WHERE user_id = ? AND balance >= ?",
                (total_price, buyer_id, total_price),
            )
            if cursor.rowcount == 0:
                return error.error_not_sufficient_funds(order_id)

            cursor = conn.execute(
                "UPDATE user set balance = balance + ?" "WHERE user_id = ?",
                (total_price, seller_id),
            )

            if cursor.rowcount == 0:
                return error.error_non_exist_user_id(seller_id)

            cursor = conn.execute(
                "DELETE FROM new_order WHERE order_id = ?", (order_id,)
            )
            if cursor.rowcount == 0:
                return error.error_invalid_order_id(order_id)

            cursor = conn.execute(
                "DELETE FROM new_order_detail where order_id = ?", (order_id,)
            )
            if cursor.rowcount == 0:
                return error.error_invalid_order_id(order_id)

            conn.commit()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))

        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            cursor = self.conn.execute(
                "SELECT password  from user where user_id=?", (user_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()

            if row[0] != password:
                return error.error_authorization_fail()

            cursor = self.conn.execute(
                "UPDATE user SET balance = balance + ? WHERE user_id = ?",
                (add_value, user_id),
            )
            if cursor.rowcount == 0:
                return error.error_non_exist_user_id(user_id)

            self.conn.commit()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
