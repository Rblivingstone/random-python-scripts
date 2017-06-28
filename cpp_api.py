# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 11:08:15 2017

@author: rbarnes
"""

from flask import jsonify,request,Flask,make_response
from flask_cors import CORS, cross_origin
from common_point_of_purchase import *

app=Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/": {"origins": "*"}})

@app.route('/top10filtered',methods=['GET'])
#@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_top_10():
    w=common_point_of_purchase('I:\\Fraud Analysis\\Fraud Analyst\\Common Point of Purchase Dashboard\\cpp.txt')
    res={}
    results=w.maximize_likelihood()
    for i in range(10):
        loc,prob=w.get_most_likely_point_of_purchase(i)
        res[loc]=prob
    return(make_response(jsonify(res)))
    #return(make_response(jsonify({'hi':'there'})))
    
if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)