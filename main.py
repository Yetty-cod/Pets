import sqlite3
from flask import Flask, request


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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)