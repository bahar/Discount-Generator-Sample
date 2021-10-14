from flask import Flask, request, abort, jsonify
import boto3
import random, string, json
from werkzeug.exceptions import NotFound

from database.helpers import *

app = Flask(__name__)


@app.route("/discounts/api/v1.0/get_code/<int:user_id>/<string:user_secret>/<int:brand_id>", methods=['GET'])
def get_discount_code(user_id=None, user_secret=None, brand_id=None):
    if not user_id or not user_secret or not brand_id:
        abort(400)
    user = find_user(user_id)
    response = None
    if user and user["user_secret"] == user_secret:
        #user is valid, so get a discount code, remove it from discounts table, add it to Used Code table
        discount_code = get_unused_discount_code(user_id)
        response = {
                'status': 'success',
                'code': '201',
                'data': discount_code,
                'message': ''
        }
    else:
        response = {
                'status': 'error',
                'code': '401',
                'data': '',
                'message': 'User ID or Secret is wrong!'
            }

    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5002, debug=True)