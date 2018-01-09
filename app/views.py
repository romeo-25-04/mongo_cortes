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
    products_list = []
    for prod in sorted_products:
        mats = prod.get('mat_consume', [])
        materials = []
        for mat in mats:
            mat_id = mat.get('id', '')
            mat_nr = mat.get('number')
            mat_name = database.get_item_by_id('products', mat_id).get('name', 'NIX')
            materials.append({'name': mat_name, 'number': mat_nr})
        prod['mat_consume'] = materials
        products_list.append(prod)
    return render_template('products.html', title='Products',
                           acProd='active',
                           products=products_list)

