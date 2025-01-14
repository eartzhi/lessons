from flask import Flask, request, jsonify
from pathlib import Path

import numpy as np
import datetime
import pickle
import os


app = Flask(__name__)

parent = Path(__file__).resolve().parent
parent = os.path.join(parent, 'models/model.pkl')


@app.route('/hello')
def hello_func():
    name = request.args.get('name')
    return f'hello, {name}!'

@app.route('/')
def index():
    return 'Test message. The server is running'

@app.route('/time')
def current_time():
    now = datetime.datetime.now()
    return f'{now.hour}:{now.minute}'
    
@app.route('/add', methods=['POST'])
def add():
    num = request.json.get('num')
    if num > 10:
        return 'too much', 400
    else:
        return jsonify({'result': num+1})
 
@app.route('/predict', methods=['POST'])
def predict():
    values = request.json
    values = np.array(values).reshape(1, 4) 
    
    with open(parent, 'rb') as pkl_file:
        model = pickle.load(pkl_file)
        
    result = model.predict(values)
    
    return jsonify({"prediction": result[0]})
    

if __name__ == '__main__':
    app.run('localhost', 5000)