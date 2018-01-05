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

new_prod = {'name': 'Plastik',
            'preis': 200,
            'gewicht': 2,
            'mat_consume': [
                {'id': '5a4e5c80b9346e13902965d0', 'number': 2}
            ]
            }
database.add_product(new_prod)
# database.delete_product_id('5a4f69fbb9346e1c9ca2f686')
