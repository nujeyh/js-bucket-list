from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.3saeh.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
from time import *


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_id = str(time())

    doc = {
        'bucket_id': bucket_id,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    id_receive = request.form['id_give']
    db.bucket.update_one({'bucket_id': str(id_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '버킷 완료!'})


@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    id_receive = request.form['id_give']
    db.bucket.update_one({'bucket_id': str(id_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '버킷 취소!'})


@app.route("/bucket/delete", methods=["POST"])
def bucket_delete():
    id_receive = request.form['id_give']
    db.bucket.delete_one({'bucket_id': str(id_receive)})
    return jsonify({'msg': '버킷 삭제!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
