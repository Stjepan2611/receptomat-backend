#importanje
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml
import os 
app = Flask(__name__)
config = yaml.load(open('database.yaml'))
client = MongoClient(config['uri'])


db = client['recept']


CORS(app)



@app.route('/api/v1/users', methods=['POST', 'GET'])
def data():
    
    # stavljanje podataka u bazu podataka (POST)
    if request.method == 'POST':
        body = request.json
        naslov = body['naslov']
        vrsta = body['vrsta']
        kuhar = body['kuhar'] 
        sastojci = body['sastojci']
        
        db['recept'].insert_one({
            "naslov": naslov,
            "vrsta": vrsta,
            "kuhar":kuhar,
            "sastojci":sastojci,
            "like":0,
            "dislike":0,
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'naslov': naslov,
            'vrsta': vrsta,
            'kuhar':kuhar,
            'sastojci':sastojci
        })
    
    # uzimanje (dohvćanje) podataka iz baze podataka (GET) 
    if request.method == 'GET':
        allData = db['recept'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            naslov = data['naslov']
            vrsta = data['vrsta']
            kuhar = data['kuhar']
            dataDict = {
                'id': str(id),
                'naslov': naslov,
                'vrsta': vrsta,
                'kuhar': kuhar,
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

# lajk dislajk
@app.route('/api/v1/rejting/<string:id>', methods=['POST'])
def likeDislike(id):
    body = request.json
    print (body)
    like = body['like']
    dislike = body['dislike']
    db['recept'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "like":like,
                    "dislike":dislike,
                    
                }
            }
    )
    return "uspjehhhh"


# komentari

@app.route('/api/v1/komentar/<string:id>', methods=['GET', 'POST'])
def komentari(id):
    if request.method == 'GET':
        data = []
        for k in db['komentari'].find({'recept_id': ObjectId(id)}):
            data.append({"koment": k["koment"]})
        print (data)
        return jsonify(data)

        # stavljanje podataka u bazu podataka (POST)

    if request.method == 'POST':
        body = request.json
        koment = body['koment'] 
        
        db['komentari'].insert_one({
            "koment": koment,
            "recept_id": ObjectId(id)
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'koment': koment
        })


@app.route('/api/v1/users/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):
    

    # dohvaćanje podataka iz baze po ID-u (GET) 

    if request.method == 'GET':
        if id == "-1":
            return "no found"
        data = db['recept'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        naslov = data['naslov']
        vrsta = data['vrsta']
        kuhar = data['kuhar']
        sastojci = data['sastojci']
        like = data['like']
        dislike = data['dislike']
        dataDict = {
            'id': str(id),
            'naslov': naslov,
            'vrsta': vrsta,
            'kuhar':kuhar,
            'sastojci':sastojci,
            'like': like,
            'dislike': dislike,
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # brisanje podataka iz baze (DELETE)
    if request.method == 'DELETE':
        db['komentari'].delete_many({'recept_id': ObjectId(id)})
        db['recept'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # ažuriranje (updejtanje) podataka u bazi (UPDATE) 
    if request.method == 'PUT':
        body = request.json
        naslov = body['naslov']
        vrsta = body['vrsta']
        kuhar = body['kuhar']
        sastojci = body['sastojci']

        db['recept'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "naslov":naslov,
                    "vrsta":vrsta,
                    "kuhar": kuhar,
                    "sastojci": sastojci,
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})


# šoping lista  

@app.route('/api/v1/CijeliPopis', methods=['POST', 'GET'])
def popis():
    
    # stavljanje podataka u bazu podataka (POST)
    if request.method == 'POST':
        body = request.json
        stavka = body['stavka'] 
        
        db['popis'].insert_one({
            "stavka": stavka
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'stavka': stavka
        })
    
    # uzimanje (dohvćanje) podataka iz baze podataka (GET) 

    if request.method == 'GET':
        allData = db['popis'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            stavka = data['stavka']
            dataDict = {
                'id': str(id),
                'stavka': stavka
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)


# update delete

@app.route('/api/v1/CijeliPopis/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onepopis(id):

    # dohvaćanje podataka iz baze po ID-u (GET) 
    if request.method == 'GET':
        if id == "-1":
            return "no found"
        data = db['popis'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        stavka = data['stavka']
        dataDict = {
            'id': str(id),
            'stavka': stavka
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # brisanje podataka iz baze (DELETE)
    if request.method == 'DELETE':
        db['popis'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # ažuriranje (updejtanje) podataka u bazi (UPDATE) 
    if request.method == 'PUT':
        body = request.json
        stavka = body['stavka']

        db['popis'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "stavka":stavka
                }
            }
        )
        return "update success"

if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0", port=int(os.environ.get("PORT",8080)))