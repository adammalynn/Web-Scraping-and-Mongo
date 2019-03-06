from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars 
import pymongo
from pprint import pprint
import time
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_dataapp"###
# mongo = PyMongo(app)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# create database
db = client.mars_db
# create collection. 
coll = db.mtable_collection

@app.route("/")
def index():
    # Get the data from mongodb.
    mars_data = coll.find_one()
    # print('inside index')
    # pprint(mars_data)
    # return template and data
    time.sleep(4)
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape function.
@app.route("/scrape")
def scraper():
    # db.coll.remove({})
    # scrape.
    marsn_data = scrape_mars.scrape()

    # Insert into database
    # coll.insert_one(marsn_data)
    coll.update({}, {"$set": marsn_data}, upsert = True)

    # Redirect to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
