from flask import Flask, request, abort, jsonify
import boto3
import random, string, json
from werkzeug.exceptions import NotFound

from database.helpers import insert_items_in_btach

app = Flask(__name__)


@app.route("/discounts/api/v1.0/generate", methods=['POST'])
def generate_code():
    if not request.json or not 'brand_id' in request.json or not 'number_of_codes' in request.json:
        abort(400)
    brand_id = request.json['brand_id']
    number_of_codes = request.json['number_of_codes']
    discount_codes = []
    for i in range(number_of_codes):
        discount_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8)) #we are generating very simple 8 character long code
        discount_codes.append({
            "code": discount_code,
            "brand_id": brand_id
        })

    #print(discount_codes)

    response = ""
    if insert_items_in_btach("Discounts", discount_codes):
        response = {
                'status': 'success',
                'code': '201',
                'data': '',
                'message': 'System generated discount codes successfully'
            }
    else:
        response = {
                'status': 'error',
                'code': '500',
                'data': '',
                'message': 'System generated discount codes successfully'
            }
    return jsonify(response)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
