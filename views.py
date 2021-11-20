from flask_restful import Resource
from flask import request, make_response
import utils
import json


class GreenPassReader(Resource):
    def post(self):
        request_body = request.json
        response = make_response(json.dumps(utils.decode_gpass(request_body['green_pass'])), 200)
        return response
