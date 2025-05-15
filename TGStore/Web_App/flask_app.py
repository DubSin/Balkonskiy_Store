from flask import Flask, render_template, request, jsonify, url_for, session
import os
import sys

sys.path.insert(1, os.getcwd())

from Data.db import DataBase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'Data', 'store.db')
db = DataBase(DB_DIR)

app = Flask(__name__, template_folder='templates') 
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv()) 
SECRET_KEY = os.getenv("SECRET_KEY")
app.secret_key = SECRET_KEY


UPLOAD_FOLDER = 'static'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/index")    
def index():  
    zip_hoodie = db.get_product('ZIP HOODIE')
    hoodie = db.get_product('HOODIE')
    sweatshirt = db.get_product('SWEATSHIRT')
    jacket = db.get_product('JACKET')
    sweater = db.get_product('SWEATER')
    zip = db.get_product('ZIP 1/4')
    shirt = db.get_product('T-SHIRT')
    sale = db.get_product('SALE')
    return render_template('index.html', zip_hoodie=zip_hoodie, hoodie=hoodie, sweatshirt=sweatshirt, jacket=jacket, sweater=sweater, zip=zip, shirt=shirt, sale=sale)  

@app.route("/product<int:slug>")
def product_page(slug):
    product = db.get_by_id(slug)
    return render_template(f"product.html", product = product)

@app.route("/search", methods=['POST'])
def search():
    search_key = request.form['find_holder']
    values = db.find_matches(search_key)
    print(values)
    return render_template('search.html', find_products=values, key=search_key)

@app.route("/order_details")
def order_page():
    return render_template("order_details.html")

@app.route('/bucket/<string:data>')
def bucket_page(data):
    total_price = 0
    newdata = []
    print(data)
    for i in data.split("|"):
        newdata.append(db.get_by_id(i))
        total_price += db.get_by_id(i)[2]
    session['data'] = newdata
    return render_template('bucket.html', products=newdata, total_price=total_price, inner_data = data)

@app.route('/process', methods = ["POST"])
def submit_bucket():
    data = '|'.join(request.get_json())
    target_url = url_for('bucket_page', data=data)
    return jsonify({'redirect': target_url})
  
if __name__ == "__main__":  
    app.run(debug=True, host = '0.0.0.0', port='8000')  