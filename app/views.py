from flask import render_template, request
from app import app
from main import Database, money

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
            materials.append({'name': mat_name, 'number': mat_nr})
        prod['mat_consume'] = materials
        prod['preis'] = money(prod['preis'])
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
