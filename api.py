# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:55:19 2020

@author: Soumitra
"""
from bson import json_util
import json
import pprint    
from pymongo import MongoClient             #python module MongoDb
url = 'mongodb://localhost:27017/'          #url for connecting to mongo server
client = MongoClient(url)
db = client.bookreview #this is a database
doc = db.doc #this is a table/collection

from flask import Flask,request, redirect, url_for, jsonify, render_template
app = Flask(__name__)



@app.route('/books', methods = ['GET'])
def indexget():
   view = db.doc.find()
   l = []
   for i in view:
       i.pop("_id")
       l.append(i)
   return jsonify(l)
    #return render_template("viewer.html",content = view, p = json.dumps)


@app.route('/books', methods = ['POST'])
def indexpost():
   args = request.args
   data = {"Name":args.get("name"),"Book":args.get("book"),"Review":args.get("review"),"Rating":args.get("rating")}
   doc.insert_one(data)
   return "<h1>Successfully posted new review.</h1>"


@app.route('/books', methods = ['PUT'])
def indexput():
   return "<h1>put operation not possible</h1>"



@app.route('/books', methods = ['DELETE'])
def indexdelete():
    db.doc.drop()
    return "<h1>Deleting all book reivews</h1>"



@app.route('/books/<username>',methods = ["GET"])
def get(username):
    data = db.doc.find_one({"Name":username})
    if(data==None):
        return f'<h1>Data for {username} does not exist!</h1>'
    else:
        data.pop("_id")
        print(f"successfully retrieved review for user {username}!")
        return data


@app.route('/books/<username>', methods = ['POST'])
def post(username):
   args = request.args
   data = {"Name":username,"Book":args.get("book"),"Review":args.get("review"),"Rating":args.get("rating")}
   doc.insert_one(data)
   return f"<h1>Successfully posted new review for user {username}</h1>"

@app.route('/books/<username>', methods = ['PUT'])
def put(username):
    args = request.args
    result = db.doc.update_one({'Name':username},{'$set':{'Review':args.get("review"),"Rating":args.get("rating")}})
    if(result.matched_count == 1 and result.modified_count == 1):
        return f"<h1>Successfully updated review for user {username}!</h1>"
    else:
        return "<h1>Failed to update!</h1>"
    
@app.route('/books/<username>', methods = ['DELETE'])
def delete(username):
    result = db.doc.delete_one({'Name':username})
    if(result.deleted_count == 1):
        return f"<h1>Successfully deleted review for user {username}!</h1>"
    else:
        return "<h1>Failed to update.</h1>"

if __name__ == '__main__':
    app.run(debug = True)
   