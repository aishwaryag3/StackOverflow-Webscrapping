import matplotlib.pyplot as plotter
import pymongo
from api_constants import password, db_name
import itertools
import numpy as np

client = pymongo.MongoClient("mongodb+srv://kathir:{}@scrappeddata.8uo7e.mongodb.net/{}?retryWrites=true&w=majority"
                             .format(password, db_name))

dbName = client[db_name]
collection = dbName["posts"]

count = 0
languages = []
for i in collection.find():
    languages.append(i["post_tag"])

lang_list = itertools.chain.from_iterable(languages)
res_lang = list(lang_list)
print(res_lang)

lang = []
lang_count = []
for i in np.unique(res_lang):
    lang.append(i)
    lang_count.append(res_lang.count(i))
    count += 1

print("Total languages are", count)


def createChart(xAxis, yAxis):
    plotter.plot(xAxis, yAxis, color='red', marker='o')
    plotter.title("Programming Languages and their usage")
    plotter.xlabel("Programming Languages", fontsize=5)
    plotter.ylabel("Number of questions")
    plotter.xticks(rotation=90)
    plotter.tick_params(axis='x', labelsize=7)
    plotter.grid(True)
    plotter.show()


start = 0
end = 50
xAxis = []
yAxis = []
for i in range(0, len(lang), 50):
    createChart(lang[start:end], lang_count[start:end])
    start += 50
    end += 50
