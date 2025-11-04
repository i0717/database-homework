from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import seller
import json

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")


@bp_seller.route("/create_store", methods=["POST"])
def seller_create_store():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    s = seller.Seller()
    code, message = s.create_store(user_id, store_id)
    return jsonify({"message": message}), code


@bp_seller.route("/add_book", methods=["POST"])
def seller_add_book():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
<<<<<<< HEAD
    book_info: dict = request.json.get("book_info")
    stock_level: int = int(request.json.get("stock_level", 0))
=======
    book_info: str = request.json.get("book_info")
    stock_level: str = request.json.get("stock_level", 0)
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc

    s = seller.Seller()
    code, message = s.add_book(
        user_id, store_id, book_info.get("id"), json.dumps(book_info), stock_level
    )
<<<<<<< HEAD
=======

>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
    return jsonify({"message": message}), code


@bp_seller.route("/add_stock_level", methods=["POST"])
def add_stock_level():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    book_id: str = request.json.get("book_id")
<<<<<<< HEAD
    add_num: int = int(request.json.get("add_stock_level", 0))

    s = seller.Seller()
    code, message = s.add_stock_level(user_id, store_id, book_id, add_num)
    return jsonify({"message": message}), code
=======
    add_num: str = request.json.get("add_stock_level", 0)

    s = seller.Seller()
    code, message = s.add_stock_level(user_id, store_id, book_id, add_num)

    return jsonify({"message": message}), code
>>>>>>> d699ef45a40f38eb8007bef2f8d99159c1ff41cc
