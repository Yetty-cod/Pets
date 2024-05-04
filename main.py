import sqlite3
from flask import Flask, request, jsonify


app = Flask(__name__)
con = sqlite3.connect('pets_db.sqlite')
cur = con.cursor()


@app.route('/application', methods=['POST'])
def application():
    name = request.args.get('name')
    surname = request.args.get('surname')
    email = request.args.get('email')
    pet = request.args.get('pet_id')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')

    if not cur.execute(f'select id from user where name = {name} and surname = {surname} and email = {email}'):
        return 'User does not exist'
    if not cur.execute(f'select * from pets where id = {pet}').fetchone():
        return 'Pet does not exist'

    cur.execute(f'insert into sittes (start_date, end_date, pet_id, sitter, waiting) values'
                f'({date_start}, {date_end}, {pet}, {-1}, {1})')
    return {'status': 'ok'}


@app.route('/register_user', methods=['POST'])
def register_user():
    name = request.args.get('name')
    surname = request.args.get('surname')
    email = request.args.get('email')

    if cur.execute(f'select * from user where name = {name} and surname = {surname} and email = {email}').fetchone():
        return 'User exist'

    cur.execute(f'insert into user (name, surname, email) values ({name}, {surname}, {email})')

    return {'status': 'ok'}


@app.route('/register_pet', methods=['POST'])
def register_pet():
    name = request.args.get('name')
    animal_type = request.args.get('animal_type')
    breed = request.args.get('breed')
    owner = request.args.get('owner')
    age = request.args.get('age')

    if cur.execute('select * from pet where name = {} and surname = {} and email = {}').fetchone():
        return 'User exist'

    cur.execute(f'insert into user (name, animal_type, breed, owner, age) values ({name}, {animal_type}, {breed}, {owner}, {age})')

    return {'status': 'ok'}


@app.route('/users_animals')
def get_animals():
    owner_name = request.args.get('owner_name')
    owner_surname = request.args.get('owner_surname')

    owner_id = cur.execute(f'select id from user where name = {owner_name} and surname = {owner_surname}')
    animals = cur.execute(f'select * from pets where owner = {owner_id}').fetchall()
    res = []
    for el in animals:
        animal_type_name = cur.execute(f'select type_name from pets_types where id = {el[2]}').fetchone()[0]
        animal_breed_name = cur.execute(f'select breed_name from breeds where id = {el[3]}').fetchone()[0]
        owner_name_surname = ' '.join(cur.execute(f'select name, surname from user where id = {el[4]}').fetchone()[0])
        res.append({'id': el[0],
                    'name': el[1],
                    'type': animal_type_name,
                    'breed': animal_breed_name,
                    'age': el[5],
                    'owner': owner_name_surname})

    return jsonify(res)


@app.route('/waiting_applications')
def get_applications():
    application = cur.execute('select * from sittes where waiting = 1').fetchall()
    res = []
    for el in application:
        pet_name = cur.execute(f'select name, animal_type, breed, age from pets where id = {}')
        res.append({'id': el[0],
                    'start_date': el[1],
                    'end_date': el[2],
                    'pet_name': pet_name,
                    'pet_type': pet_type,
                    'pet_breed': pet_breed,
                    'pet_age': pet_age})

    return jsonify(res)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)