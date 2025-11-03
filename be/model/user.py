import jwt
import time
import logging
from be.model import error
from be.model import db_conn


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded


def jwt_decode(encoded_token, user_id: str) -> dict:
    return jwt.decode(encoded_token, key=user_id, algorithms=["HS256"])


class User(db_conn.DBConn):
    token_lifetime: int = 3600  # 3600秒有效期

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            now = time.time()
            return 0 <= now - ts <= self.token_lifetime
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            if self.user_id_exist(user_id):
                return error.error_exist_user_id(user_id)

            terminal = f"terminal_{time.time()}"
            token = jwt_encode(user_id, terminal)
            self.db.user.insert_one({
                'user_id': user_id,
                'password': password,
                'balance': 0,
                'token': token,
                'terminal': terminal
            })
            return 200, "ok"
        except Exception as e:
            logging.error(f"注册失败: {e}")
            return 528, f"{str(e)}"

    def check_token(self, user_id: str, token: str) -> (int, str):
        user = self.db.user.find_one({'user_id': user_id})
        if not user:
            return error.error_authorization_fail()
        if not self.__check_token(user_id, user['token'], token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> (int, str):
        user = self.db.user.find_one({'user_id': user_id})
        if not user or user['password'] != password:
            return error.error_authorization_fail()
        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        try:
            code, msg = self.check_password(user_id, password)
            if code != 200:
                return code, msg, ""

            token = jwt_encode(user_id, terminal)
            result = self.db.user.update_one(
                {'user_id': user_id},
                {'$set': {'token': token, 'terminal': terminal}}
            )
            if result.modified_count == 0:
                return error.error_authorization_fail() + ("",)
            return 200, "ok", token
        except Exception as e:
            return 528, f"{str(e)}", ""

    def logout(self, user_id: str, token: str) -> (int, str):
        try:
            code, msg = self.check_token(user_id, token)
            if code != 200:
                return code, msg

            terminal = f"terminal_{time.time()}"
            dummy_token = jwt_encode(user_id, terminal)
            result = self.db.user.update_one(
                {'user_id': user_id},
                {'$set': {'token': dummy_token, 'terminal': terminal}}
            )
            if result.modified_count == 0:
                return error.error_authorization_fail()
            return 200, "ok"
        except Exception as e:
            return 528, f"{str(e)}"

    def unregister(self, user_id: str, password: str) -> (int, str):
        try:
            code, msg = self.check_password(user_id, password)
            if code != 200:
                return code, msg

            result = self.db.user.delete_one({'user_id': user_id})
            if result.deleted_count == 0:
                return error.error_authorization_fail()
            return 200, "ok"
        except Exception as e:
            return 528, f"{str(e)}"

    def change_password(
            self, user_id: str, old_password: str, new_password: str
    ) -> (int, str):
        try:
            code, msg = self.check_password(user_id, old_password)
            if code != 200:
                return code, msg

            terminal = f"terminal_{time.time()}"
            token = jwt_encode(user_id, terminal)
            result = self.db.user.update_one(
                {'user_id': user_id},
                {'$set': {
                    'password': new_password,
                    'token': token,
                    'terminal': terminal
                }}
            )
            if result.modified_count == 0:
                return error.error_authorization_fail()
            return 200, "ok"
        except Exception as e:
            return 528, f"{str(e)}"