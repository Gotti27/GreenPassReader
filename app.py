from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import views

app = Flask('GreenPassReader')
api = Api(app)

api.add_resource(views.GreenPassReader, '/gpass')

if __name__ == '__main__':
    app.run(debug=True)

