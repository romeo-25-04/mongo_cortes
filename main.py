import pprint
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId

pp = pprint.PrettyPrinter(indent=2)


class Database:
    VEHICLE_KEYS = ['kaufpreis', 'marke', 'max_load', 'max_speed', 'mietpreis',
                    'panzerung', 'passagiere', 'pferdest', 'tank', 'veh_type']
    PRODUCT_KEYS = ['name', 'preis', 'gewicht', 'mat_consume']

    def __init__(self, user, password):
        self.client = MongoClient(
            'mongodb://{}:{}@ds161336.mlab.com:61336/michecortes_db'.format(
                user, password)
        )
        self.db = self.client['michecortes_db']
        self.vehicles_col = self.db['vehicles']
        self.products_col = self.db['products']

    def add_vehicle(self, veh):
        valid = False
        for key in self.VEHICLE_KEYS:
            if key in veh.keys():
                valid = True
            else:
                valid = False
                break
        if valid:
            inserted_id = self.vehicles_col.insert_one(veh).inserted_id
        else:
            inserted_id = None
        return inserted_id

    def delete_vehicle_ID(self, id_str):
        self.vehicles_col.delete_one({'_id': ObjectId(id_str)})

    def add_product(self, prod):
        valid = False
        for key in self.PRODUCT_KEYS:
            if key in prod.keys():
                valid = True
            else:
                valid = False
                break
        if valid:
            inserted_id = self.products_col.insert_one(prod).inserted_id
        else:
            inserted_id = None
        return inserted_id

    def delete_product_id(self, id_str):
        self.products_col.delete_one({'_id': ObjectId(id_str)})

    def get_item_by_id(self, col_name, id_str):
        return self.db[col_name].find_one({'_id': ObjectId(id_str)})


def main():
    database = Database('main_amareto', 'michepass')
    print(database.db.collection_names(include_system_collections=False))
    print(database.products_col)
    new_veh = {'kaufpreis': 0,
           'marke': 'Test Auto',
           'max_load': 10000,
           'max_speed': 500,
           'mietpreis': 123000,
           'panzerung': 200,
           'passagiere': 55,
           'pferdest': 232,
           'tank': 1000,
           'veh_type': 'PKW'}
    # ADD DELETE TEST
    # database.add_vehicle(new_veh)
    # database.delete_vehicle_ID('5a4cfae4b9346e12c8167eb6')

    new_prod = {'name': 'LSD',
                'preis': 7000,
                'gewicht': 2,
                'mat_consume': [
                    {'id': '', 'number': 2}
                ]
                }
    # database.add_product(new_prod)
    database.delete_product_id('5a4e5f2cb9346e1e4056eb99')


    print('_'*61)
    print('{:30} | {:9} | {:5} | {:5} | {}'.format(
        'MARKE',
        'KAUFPREIS',
        'KOFFERRAUM',
        'TYP',
        'ID'
    ))
    print('-'*61)
    sorted_vehicles = database.vehicles_col.find().sort([
        ('max_load', ASCENDING)
    ])
    for auto in sorted_vehicles:
        print('{:30} | {:9} | {:10} | {:5} | {}'.format(
            auto.get('marke', 'NIX'),
            auto.get('kaufpreis', 'NIX'),
            auto.get('max_load', 'NIX'),
            auto.get('veh_type', 'NIX'),
            auto.get('_id', 'NIX')
        ))
        # pp.pprint(auto)
    
    print('-'*61)
    
    print('_'*61)
    print('{:20} | {:7} | {:7} | {:20} | {}'.format(
        'NAME', 'PREIS', 'GEWICHT', 'MATERIALS', 'ID'
    ))
    sorted_prods = database.products_col.find().sort([
        ('name', ASCENDING)
    ])
    for prod in sorted_prods:
        print('{:20} | {:7} | {:7} | {} | {}'.format(
            prod.get('name', 'NIX'),
            prod.get('preis', 'NIX'),
            prod.get('gewicht', 'NIX'),
            prod.get('mat_consume', []),
            str(prod.get('_id', 'NIX'))
        ))
    print('-'*61)
    
    
    def chain_route(veh, prod):
        empty_load = veh.get('max_load', 0)
        mats = prod.get('mat_consume', {})
        mat1_id = 0
        mat1_consume = mats[0]
        component = database.get_item_by_id('products', mat1_id)

        pieces = empty_load / component.get('gewicht', 1)
        pieces = int(pieces / mat1_consume)
    
        for mat_id, mat_consume in mats[1:]:
            component = database.get_item_by_id('products', mat_id)
            pieces = int(pieces / mat_consume)
            print(empty_load, pieces)
        receipt = pieces * prod.get('preis', 0)
        print('{} with {} can make {} pieces. Receipt:${}'.format(
            prod.get('name', 'NIX'), veh.get('marke', 'Nix'), pieces,  int(receipt*0.5 + receipt)
        ))
    
    hemmt = database.get_item_by_id('vehicles', '5a3b9bffb9346e15603fe81c')
    
    # lsd = database.get_item_by_id('products', '5a4e5f84b9346e1cc40abc87')
    # plastik = database.get_item_by_id('products', '5a4e5f2cb9346e1e4056eb99')
    #
    # chain_route(hemmt, plastik)


if __name__ == '__main__':
    main()
