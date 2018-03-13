from flask import render_template, request, redirect, jsonify
from app import app
from app.logic.main import Database, money
import pprint
from .forms import ButtonForm

db_user = app.config['MLAB_USER']
db_password = app.config['MLAB_PASSWORD']
database = Database(db_user, db_password)


def get_vehicles():
    sorted_vehicles = database.vehicles_col.find().sort([
        ('max_load', 1)
    ])
    vehicles = []
    for auto in sorted_vehicles:
        auto['kaufpreis'] = money(auto['kaufpreis'])
        vehicles.append(auto)
    return vehicles


def get_products(filter_ids=[]):
    if filter_ids:
        found_products = database.get_items_by_id_list('products', filter_ids)
    else:
        found_products = database.products_col.find()
    sorted_products = found_products.sort([
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
            materials.append({'name': mat_name, 'number': mat_nr, 'id': mat_id})
        prod['mat_consume'] = materials
        prod['preis_html'] = money(prod['preis'])
        products_list.append(prod)
    return products_list


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="General", acHome='active')


@app.route('/vehicles')
def vehicles():
    add_button_form = ButtonForm()
    return render_template('vehicles.html',
                           title='Vehicles',
                           acVeh='active',
                           vehicles=get_vehicles(),
                           add_button_form=add_button_form,
                           admin=False)


@app.route('/products', methods=['GET', 'POST'])
def products():
    result = []
    if request.method == "POST":
        result = request.form.getlist("product")
    return render_template('products.html', title='Products',
                           acProd='active',
                           products=get_products(result),
                           all_products=get_products(),
                           admin=False)


@app.route('/route', methods=['GET', 'POST'])
def route():
    products = get_products()
    vehicles = get_vehicles()
    result = {'name': 'Select a Product',
              'marke': 'Select a Vehicle',
              'pieces': 0, 'receipt': 0, 'info': []}
    if request.method == 'POST':
        result = request.form
        veh_id = result.get('Vehicle', 'NIX')
        prod_id = result.get('Product', 'NIX')
        name, marke, pieces, receipt, info = database.route_calc(veh_id, prod_id)

        result = {'name': name, 'marke': marke,
                  'pieces': pieces, 'receipt': receipt, 'info': info}
    else:
        pass
    return render_template('route.html', title='Route',
                           acRoute='active',
                           vehicles=vehicles,
                           products=products,
                           result=result,
                           admin=False)


@app.route('/add_vehicle', methods=['GET', 'POST'])
@app.route('/update_vehicle/<veh_id>', methods=['GET', 'POST'])
def add_update_vehicle(veh_id=None):
    if veh_id:
        new_veh = database.get_item_by_id('vehicles', veh_id)
    else:
        new_veh = {'kaufpreis': 100,
                   'marke': 'Test',
                   'max_load': 100,
                   'max_speed': 120,
                   'mietpreis': 50,
                   'panzerung': 30,
                   'passagiere': 1,
                   'pferdest': 100,
                   'tank': 30,
                   'veh_type': 'PKW'}
    if request.method == 'GET':
        return render_template('vehicle_form.html', title='Add / Update Vehicle',
                               new_veh=new_veh)
    elif request.method == 'POST':
        result = request.form
        new_veh = {'kaufpreis': int(result.get('kaufpreis', 22)),
                   'marke': result.get('marke', 'NIX'),
                   'max_load': int(result.get('max_load', 22)),
                   'max_speed': int(result.get('max_speed', 22)),
                   'mietpreis': int(result.get('mietpreis', 22)),
                   'panzerung': int(result.get('kaufpreis', 22)),
                   'passagiere': int(result.get('passagiere', 22)),
                   'pferdest': int(result.get('pferdest', 22)),
                   'tank': int(result.get('tank', 22)),
                   'veh_type': result.get('veh_type', 'PKW')}
        if veh_id:
            for key, value in new_veh.items():
                database.update_itemfield_by_id('vehicles', veh_id, key, value)
        else:
            database.add_vehicle(new_veh)
    return redirect('/vehicles')


@app.route('/delete_vehicle/<veh_id>')
def delete_vehicle(veh_id):
    database.delete_vehicle_ID(veh_id)
    return redirect('/vehicles')


@app.route('/add_product', methods=['GET', 'POST'])
@app.route('/update_product/<prod_id>', methods=['GET', 'POST'])
def add_update_product(prod_id=None):
    new_prod = {'name': 'Test_Product',
                'preis': 5,
                'gewicht': 2,
                'mat_consume': []
                }
    if prod_id:
        new_prod = database.get_item_by_id('products', prod_id)

    if request.method == "GET":
        return render_template('product_form.html', title='Add / Update Product',
                               products=get_products(),
                               new_prod=new_prod)
    else:
        result = request.form
        materials_id = result.getlist('materials_id[]')
        materials_nr = result.getlist('materials_nr[]')
        materials = [
            {'id': materials_id[i], 'number': int(materials_nr[i])}
            for i in range(len(materials_id))
            if materials_nr[i] != '' and materials_id[i] != ''
        ]
        new_prod = {'name': result.get('name', 'NIX'),
                    'preis': int(result.get('preis', 22)),
                    'gewicht': int(result.get('gewicht', 22)),
                    'mat_consume': materials
                    }
        if prod_id:
            for key, value in new_prod.items():
                database.update_itemfield_by_id('products', prod_id, key, value)
        else:
            database.add_product(new_prod)
        return redirect('/products')


@app.route('/delete_product/<prod_id>')
def delete_product(prod_id):
    database.delete_product_id(prod_id)
    return redirect('/products')


def get_materials(prod_id, number=1, freq=dict()):
    prod = database.get_item_by_id('products', prod_id)
    materials = prod.get('mat_consume', [])
    crafting = []
    freq = freq
    for mat in materials:
        mat_id = mat.get('id')
        mat_nr = mat.get('number')
        mat_db = database.get_item_by_id('products', mat_id)
        mat_name = mat_db.get('name')
        mat_consume, freq = get_materials(mat_id, number=mat_nr * number, freq=freq)
        new_mat = {
            'name': mat_name,
            'number': mat_nr * number,
            'mat_consume': mat_consume
        }
        if len(mat_consume) == 0:
            if mat_name in freq:
                freq[mat_name] += mat_nr * number
            else:
                freq[mat_name] = mat_nr * number
        crafting.append(new_mat)
    return crafting, freq


@app.route('/crafting/<prod_id>/<int:number>')
def show_materials(prod_id=None, number=1):
    product = dict()
    freq = dict()
    if prod_id:
        prod = database.get_item_by_id('products', prod_id)
        mat_consume, freq = get_materials(prod_id=prod_id, number=number, freq=freq)
        product = {
            'name': prod.get('name'),
            'number': number,
            'mat_consume': mat_consume
        }
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    summ_pieces = sum([val for key, val in sorted_freq])
    return render_template('crafting.html', title='Crafting ' + product.get('name', ''),
                           product=product, raw_materials=sorted_freq,
                           summ_pieces=money(summ_pieces), summ_place=money(summ_pieces * 2))

@app.route('/store')
def store():

    return render_template('store.html', title='Warehouse Logistics')
