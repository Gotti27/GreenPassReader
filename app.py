from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import views

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')
api = Api(app)

api.add_resource(views.GreenPassReader, '/greenpass')

if __name__ == '__main__':
    app.run()

