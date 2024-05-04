import sqlite3
from flask import Flask, request, jsonify, make_response


app = Flask(__name__)
con = sqlite3.connect('pets_db.sqlite')
cur = con.cursor()


@app.route('/application', methods=['POST'])
def application():
    '''
    Создание заяаки о передержке
    :return:
    '''
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
    '''
    Зарегистрировать нового пользователя
    :return: cookie
    '''
    name = request.args.get('name')
    surname = request.args.get('surname')
    email = request.args.get('email')

    if cur.execute(f'select * from user where name = {name} and surname = {surname} and email = {email}').fetchone():
        return 'User exist'

    cur.execute(f'insert into user (name, surname, email) values ({name}, {surname}, {email})')

    res = make_response({'status': 'ok'})
    user_id = cur.execute(f'select id from user where name = {name} and surname = {surname} and email = {email}').fetchone()[0]
    res.set_cookie('user_id', user_id)

    return res


@app.route('/register_pet', methods=['POST'])
def register_pet():
    '''
    Зарегистрировать нового питомца
    :return:
    '''
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
    '''
    Получить питосцев владельца
    :return: список json
    '''
    owner_id = request.cookies.get('user_id')
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
    '''
    Получить активные заявки на передержку
    :return: список json
    '''
    application = cur.execute('select * from sittes'
                              'join pets on sittes.pet_id = pets.id'
                              'join pets_types on pets.animal_type = pets_types.id'
                              'join breeds on pets.breed = breeds.id where waiting = 1').fetchall()
    res = []
    for el in application:
        res.append({'id': el[0],
                    'start_date': el[1],
                    'end_date': el[2],
                    'pet_name': el[7],
                    'pet_type': el[-3],
                    'pet_breed': el[-1],
                    'pet_age': el[-5]})

    return jsonify(res)


@app.route('/accept_application')
def accept_application():
    '''
    Принять заявку о передержке
    :return:
    '''
    user_id = request.cookies.get('user_id')
    sittes_id = request.args.get('sittes_id')
    cur.execute(f'update sittes set sitter = {user_id}, waiting = 0 where id = {sittes_id}')
    return {'status': 'ok'}


@app.route('/login')
def accept_application():
    '''
    Войти
    :return: новые cookie
    '''
    name = request.args.get('name')
    surname = request.args.get('surname')
    email = request.args.get('email')

    user_id = cur.execute(f'select id from user where name = {name} and surname = {surname} and email = {email}').fetchone()
    if user_id:
        user_id = user_id[0]
        res = make_response({'status': 'ok'})
        res.set_cookie('user_id', user_id)
        return res
    else:
        return 'User does not exist'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
