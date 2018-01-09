from flask import render_template, request
from app import app
from main import Database

database = Database('main_amareto', 'michepass')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="General", acHome='active')


@app.route('/vehicles')
def vehicles():
    sorted_vehicles = database.vehicles_col.find().sort([
        ('max_load', 1)
    ])
    sorted_vehicles = [auto for auto in sorted_vehicles]
    return render_template('vehicles.html',
                           title='Vehicles',
                           acVeh='active',
                           vehicles=sorted_vehicles)


@app.route('/products')
def products():
    sorted_products = database.products_col.find().sort([
        ('name', 1)
    ])
    sorted_products = [prod for prod in sorted_products]
    return render_template('products.html', title='Products',
                           acProd='active',
                           products=sorted_products)

