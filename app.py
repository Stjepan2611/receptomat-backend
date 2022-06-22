#importanje
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml

app = Flask(__name__)
config = yaml.load(open('database.yaml'))
client = MongoClient(config['uri'])
# db = client.lin_flask
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
        # db.recept.insert_one({
        db['recept'].insert_one({
            "naslov": naslov,
            "vrsta": vrsta,
            "kuhar":kuhar
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'naslov': naslov,
            'vrsta': vrsta,
            'kuhar':kuhar
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
                'kuhar': kuhar
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)

@app.route('/api/v1/users/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # dohvaćanje podataka iz baze po ID-u (GET) 
    if request.method == 'GET':
        data = db['recept'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        naslov = data['naslov']
        vrsta = data['vrsta']
        kuhar = data['kuhar']
        dataDict = {
            'id': str(id),
            'naslov': naslov,
            'vrsta': vrsta,
            'kuhar':kuhar
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # brisanje podataka iz baze (DELETE)
    if request.method == 'DELETE':
        db['recept'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # ažuriranje (updejtanje) podataka u bazi (UPDATE) 
    if request.method == 'PUT':
        body = request.json
        naslov = body['naslov']
        vrsta = body['vrsta']
        kuhar = body['kuhar']

        db['recept'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "naslov":naslov,
                    "vrsta":vrsta,
                    "kuhar": kuhar
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})

if __name__ == '__main__':
    app.debug = True
    app.run(host = "0.0.0.0")