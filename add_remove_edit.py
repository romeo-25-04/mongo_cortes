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
# database.delete_vehicle_ID('5a4cfae4b9346e12c8167eb6')

new_prod = {'name': 'Gold',
            'preis': 1350,
            'gewicht': 2,
            'mat_consume': [
                {'id': '5a560f9d8c88be0f80d49d87', 'number': 2}
            ]
            }
# database.add_product(new_prod)
# database.delete_product_id('5a4f69fbb9346e1c9ca2f686')
database.update_itemfield_by_id('vehicles', '5a587607b9346e1da4942ead', 'max_load', 2400)
