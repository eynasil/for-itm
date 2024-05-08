from flask import Flask
dental = Flask(__name__)

@dental.route('/')
def hello_world():
    return 'Hello, World!'
