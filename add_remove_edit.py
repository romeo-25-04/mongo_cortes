from main import Database

database = Database('main_amareto', 'michepass')

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

new_prod = {'name': 'Kupferbaren',
            'preis': 300,
            'gewicht': 2,
            'mat_consume': [
                {'id': '5a4e5c64b9346e0658f3fe84', 'number': 2}
            ]
            }
# database.add_product(new_prod)
# database.delete_product_id('5a4f69fbb9346e1c9ca2f686')
database.update_itemfield_by_id('products', '5a4f69d1b9346e12bc2b0476', 'preis', 14000)
