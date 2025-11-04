import uuid
import json
import logging
from be.model import db_conn
from be.model import error


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)

    def new_order(
            self, user_id: str, store_id: str, id_and_count: [(str, int)]
    ) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)

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