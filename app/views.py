from flask import render_template, request, redirect
from app import app
from main import Database, money
from bson import ObjectId

database = Database('main_amareto', 'michepass')


def get_vehicles():
    sorted_vehicles = database.vehicles_col.find().sort([
        ('max_load', 1)
    ])
    vehicles = []
    for auto in sorted_vehicles:
        auto['kaufpreis'] = money(auto['kaufpreis'])
        vehicles.append(auto)
    return vehicles


def get_products():
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
    return render_template('vehicles.html',
                           title='Vehicles',
                           acVeh='active',
                           vehicles=get_vehicles())


@app.route('/products')
def products():
    return render_template('products.html', title='Products',
                           acProd='active',
                           products=get_products())


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
                           result=result)


@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    template_veh = {'kaufpreis': 100,
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
                               new_veh=template_veh)
    else:
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
        database.add_vehicle(new_veh)
        return redirect('/vehicles')


@app.route('/update_vehicle/<veh_id>', methods=['GET', 'POST'])
def update_vehicle(veh_id):
    veh = database.get_item_by_id('vehicles', veh_id)
    if request.method == 'GET':
        return render_template('vehicle_form.html', title='Add / Update Vehicle',
                               new_veh=veh)
    else:
        result = request.form
        updated_veh = {'kaufpreis': int(result.get('kaufpreis', 22)),
                       'marke': result.get('marke', 'NIX'),
                       'max_load': int(result.get('max_load', 22)),
                       'max_speed': int(result.get('max_speed', 22)),
                       'mietpreis': int(result.get('mietpreis', 22)),
                       'panzerung': int(result.get('kaufpreis', 22)),
                       'passagiere': int(result.get('passagiere', 22)),
                       'pferdest': int(result.get('pferdest', 22)),
                       'tank': int(result.get('tank', 22)),
                       'veh_type': result.get('veh_type', 'PKW')}
        for key, value in updated_veh.items():
            database.update_itemfield_by_id('vehicles', veh_id, key, value)
        return redirect('/vehicles')


@app.route('/delete_vehicle/<veh_id>')
def delete_vehicle(veh_id):
    database.delete_vehicle_ID(veh_id)
    return redirect('/vehicles')
