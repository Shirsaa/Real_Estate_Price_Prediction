from flask import Flask
from flask import request, url_for, jsonify, jsonify
from flask.templating import render_template
from flask import session
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
import mysql
from flask_migrate import Migrate, migrate
from sqlalchemy import select
from flask import json
from flask_mysqldb import MySQL
import util


app = Flask(__name__)
app.debug = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'customer_preferences'

mysql = MySQL(app)


@app.route('/')
def index():
    location_list = util.get_location_name() 
    print("one")
    return render_template('index.html', location_list=location_list)

@app.route('/submition', methods=['GET', 'POST'])
def answers():
    
    location_list = util.get_location_name()
    print("two")
    
    data = request.get_json()
    print(data)

    total_sqft = data['Squareft']
    location_1 = data['uiLocations']
    bhk_1 = data['uiBHK']
    bath_1 = data['uiBathrooms'] 

    price = util.estimated_price(location_1, total_sqft, bath_1, bhk_1)
    price = round(price, 3)

    info = (total_sqft, location_1, bhk_1, bath_1, price)

    query_insert = "INSERT INTO estimates (Area, Location, BHK, Bathroom, Price) VALUES (%s,%s,%s,%s,%s)"

    cur = mysql.connection.cursor()
    cur.execute(query_insert, info)

    mysql.connection.commit()
    cur.close()
    
    print(price)
    
    return jsonify(price)

if __name__ == '__main__':
    app.run()
