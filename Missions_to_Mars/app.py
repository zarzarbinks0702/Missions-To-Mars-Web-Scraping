from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    #find one record from the mars database
    mars_data = mongo.db.collection.find_one()
    #return template and render data
    return render_template("index.html", mars_data=mars_data)

@app.route('/scrape')
def scraper():
    #scrape the mars data
    mars_info = scrape_mars.scrape()
    #update mongo collection
    mongo.db.collection.update({}, mars_info, upsert=True)
    #redirect home
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
