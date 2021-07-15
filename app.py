from flask import Flask
from flask import jsonify
from flask_pymongo import PyMongo
from api_constants import password, db_name

app = Flask(__name__)

db_uri = "mongodb+srv://kathir:{}@scrappeddata.8uo7e.mongodb.net/{}?retryWrites=true&w=majority".format(password,
                                                                                                        db_name)
app.config['MONGO_DBNAME'] = db_name
app.config['MONGO_URI'] = db_uri

mongo = PyMongo(app)

@app.route('/api/test', methods=["GET"])
def test():
    return jsonify("kathir", 200)


@app.route('/api/questions', methods=["GET"])
def get_questions():
    questions = mongo.db.posts
    results = []
    for i in questions.find():
        results.append({
            "doc_id": i["doc_id"],
            "question": i["question"],
            "views": i["views"],
            "vote_count": i["vote_count"],
            "post_tag": i["post_tag"],
            "asked_by": i["asked_by"],
            "avatar": i["avatar"],
        })
    return jsonify({'result': results})


@app.route('/api/questions/tag/<tagName>', methods=["GET"])
def get_tagDetails(tagName):
    questions = mongo.db.posts
    count = 0
    results = []
    for i in questions.find({"post_tag": tagName}):
        results.append({
            "question": i["question"],
            "views": i["views"],
            "vote_count": i["vote_count"],
            "post_tag": i["post_tag"],
            "asked_by": i["asked_by"],
            "avatar": i["avatar"],
        })
        count += 1

    print("Total count", count)
    return jsonify({'result': results})


@app.route('/api/questions/tagcount/<tagName>', methods=["GET"])
def get_tagCount(tagName):
    questions = mongo.db.posts
    count = 0
    for i in questions.find({"post_tag": tagName}):
        count += 1

    return jsonify({'tag-count': count})


if __name__ == '__main__':
    app.run()
