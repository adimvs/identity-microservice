from flask import Flask, jsonify, request, json
import os
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

person = {'first_name': 'Bill',
     'last_name': 'Gates',
     'series': 'RX',
     'number': '234987',
     'cnp': '1600011223344',
     'document_image':'',
     'selfie_image':''}

@app.route("/")
def hello_world():
    return "Hello World!"

# A route to return all of the available identities in our catalog.
@app.route('/api/v1/resources/identities', methods=['GET'])
def api_all():
    res_id = request.url.rsplit('/', 1)[1]
    username = os.environ.get("USER")
    password = os.environ.get("PASS")
    myclient = pymongo.MongoClient("mongodb://%s:%s@mongodb:27017/" % (username,password))
    mydb = myclient["peopledb"]

    mycol = mydb["identities"]
    
    myid = mycol.find_one({'_id': ObjectId(res_id)})

    
    return jsonify(myid)

# A route save a new identity.
@app.route('/api/v1/resources/identities', methods=['POST'])
def api_test():
    #mongodb:27017
    username = os.environ.get("USER")
    password = os.environ.get("PASS")
    myclient = pymongo.MongoClient("mongodb://%s:%s@mongodb:27017/" % (username,password))
    mydb = myclient["peopledb"]

    mycol = mydb["identities"]
    
    x = mycol.insert_one(person)
    
    print(x.inserted_id)
    
    response = {'id': '%s' % x.inserted_id}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
