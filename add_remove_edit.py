import argparse
from main import Database

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--user')
parser.add_argument('--password')
args = parser.parse_args()

database = Database(args.user, args.password)

new_veh = {'kaufpreis': 400000,
           'marke': 'Renault Midlum',
           'max_load': 800,
           'max_speed': 112,
           'mietpreis': 200000,
           'panzerung': 100,
           'passagiere': 2,
           'pferdest': 450,
           'tank': 500,
           'veh_type': 'LKW'}
# ADD DELETE TEST
# database.add_vehicle(new_veh)
# database.delete_vehicle_ID('5a4cfae4b9346e12c8167eb6')

new_prod = {'name': 'Elektroteile',
            'preis': 90000,
            'gewicht': 2,
            'mat_consume': [
                {'id': '5a4f743eb9346e0f185515bb', 'number': 4},
                {'id': '5a4f7468b9346e0b0ca8aba3', 'number': 2},
                {'id': '5a4f6fe3b9346e1cf42de7c0', 'number': 6}
            ]
            }
# database.add_product(new_prod)
# database.delete_product_id('5a4f69fbb9346e1c9ca2f686')
# database.update_itemfield_by_id('products', '5a4f69d1b9346e12bc2b0476', 'preis', 14000)
