from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrapemars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mdata_app")

@app.route("/")
def home():
    d_data = mongo.db.collection.find_one()
    return render_template("index.html", mdata=d_data)

@app.route("/scrape")
def scrape():
    data = scrapemars.scrape()
    mongo.db.collection.update({}, data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)