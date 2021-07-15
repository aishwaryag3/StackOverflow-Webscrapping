import requests
from bs4 import BeautifulSoup
import json
import pymongo
from api_constants import password, db_name

client = pymongo.MongoClient("mongodb+srv://kathir:{}@scrappeddata.8uo7e.mongodb.net/{}?retryWrites=true&w=majority".format(password, db_name))

dbName = client[db_name]
collection = dbName["posts"]

res = requests.get("https://stackoverflow.com/questions")
soup = BeautifulSoup(res.text, "html.parser")
questions = soup.select(".question-summary")

questions_data = []
count = 0
field_names = ["question", "views", "vote_count", "post_tag", "time", "asked_by", "avatar"]

for question in questions:
    q = question.select_one(".question-hyperlink").getText()
    vote = question.select_one(".vote-count-post").getText()
    post_tag = [i.getText() for i in (question.select('.post-tag'))]
    views = question.select_one(".views").attrs['title']
    asked_by = question.select_one(".user-details").a.getText()
    avatar = question.select_one(".user-gravatar32").a.attrs["href"]

    questions_data.append({
        "question": q,
        "views": views,
        "vote_count": vote,
        "post_tag": post_tag,
        "asked_by": asked_by,
        "avatar": avatar
    })
    count += 1

json_data = json.dumps(questions_data)
print(json_data)
print(count)

collection.insert_many(questions_data)


# pd.read_json(json_data).to_csv("output.csv")