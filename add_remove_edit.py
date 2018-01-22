import argparse
from main import Database

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--user')
parser.add_argument('--password')
args = parser.parse_args()

database = Database(args.user, args.password)

new_veh = {'kaufpreis': 100000000,
           'marke': 'V-44 Blackfish',
           'max_load': 5000,
           'max_speed': 620,
           'mietpreis': 50000000,
           'panzerung': 400,
           'passagiere': 3,
           'pferdest': 1200,
           'tank': 2000,
           'veh_type': 'Flugzeug'}
# ADD DELETE TEST
# database.add_vehicle(new_veh)
database.delete_vehicle_ID('5a65c2bcb9346e215c35b31e')

new_prod = {'name': 'Elektrostühle',
            'preis': 560000,
            'gewicht': 2,
            'mat_consume': [
                {'id': '5a4f743eb9346e0f185515bb', 'number': 2},
                {'id': '5a5cf1bf8c88be1c7c4462d5', 'number': 1},
                {'id': '5a4f6fe3b9346e1cf42de7c0', 'number': 3},
                {'id': '5a53492ab9346e07a4c78e79', 'number': 2}
            ]
            }
# database.add_product(new_prod)
# database.delete_product_id('5a4f69fbb9346e1c9ca2f686')
# database.update_itemfield_by_id('vehicles', '5a587607b9346e1da4942ead', 'max_load', 2400)
