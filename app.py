from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

from Forms.FestForm import FestForm
from Forms.FestFormEdit import FestFormEdit
from Forms.LoginForm import LoginForm
from Forms.PeopleFormEdit import PeopleFormEdit
from Forms.RegistrationFrom import RegistrationForm
from Forms.SearchForm import SearchForm
import os

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contest(db.Model):
    tablename = 'contest'
    contest_name = db.Column(db.String(300), primary_key=True)
    fest_name = db.Column(db.String(20), db.ForeignKey('fest.fest_name'))


class People(db.Model):
    tablename = 'People'
    people_email = db.Column(db.String(20), primary_key=True)
    people_name = db.Column(db.String(20))
    people_phone = db.Column(db.String(20))
    people_birthday = db.Column(db.Date)
    people_password = db.Column(db.String(20))

    people_fest = db.relationship('Fest')


class association(db.Model):
    __tablename__ = 'associate_table'
    left_name = db.Column(db.String(20), db.ForeignKey('fest.fest_name'), primary_key=True)
    right_name = db.Column(db.String(20), db.ForeignKey('place.place_name'), primary_key=True)


class Fest(db.Model):
    __tablename__ = 'fest'
    fest_name = db.Column(db.String(20), primary_key=True)
    people_email = db.Column(db.String(20), db.ForeignKey('people.people_email'))
    fest_date = db.Column(db.Date)

    place_name_fk = db.relationship("Place", secondary='associate_table')
    fest_contest = db.relationship('Contest')


class CityHasPlace(db.Model):
    __tablename__ = 'city_has_place'
    place_name = db.Column(db.String(20), db.ForeignKey('place.place_name'), primary_key=True)
    city_name = db.Column(db.String(20), db.ForeignKey('city.city_name'), primary_key=True)


class Place(db.Model):
    __tablename__ = 'place'
    place_name = db.Column(db.String(20), primary_key=True)
    place_adress = db.Column(db.String(100))
    place_price = db.Column(db.Integer)

    fest_name_fk = db.relationship("Fest", secondary='associate_table')

    city_name_fk = db.relationship("City", secondary='city_has_place')


class City(db.Model):
    __tablename__ = 'city'
    city_name = db.Column(db.String(20), primary_key=True)
    city_population = db.Column(db.Integer)
    city_balance = db.Column(db.Integer)

    place_name_fk = db.relationship('Place', secondary='city_has_place')


# создание всех таблиц
db.create_all()

#очистка всех таблиц
db.session.query(CityHasPlace).delete()
db.session.query(City).delete()
db.session.query(association).delete()
db.session.query(Contest).delete()
db.session.query(Fest).delete()
db.session.query(People).delete()
db.session.query(Place).delete()


aaa = People(people_email='aaa@gmail.com',
             people_name='aaa',
             people_phone='0987845678',
             people_birthday="1995-01-23",
             people_password='aaa123'
             )

bbb = People(people_email='bbb@gmail.com',
             people_name='bbb',
             people_phone='0945698736',
             people_birthday='1987-2-21',
             people_password='bbb123'
             )

ccc = People(people_email='ccc@gmail.com',
             people_name='ccc',
             people_phone='0984587634',
             people_birthday='1967-6-23',
             people_password='ccc123'
             )

ddd = People(people_email='ddd@gmail.com',
             people_name='ddd',
             people_phone='0874987595',
             people_birthday='2001-1-1',
             people_password='ddd123'
             )

eee = People(people_email='eee@gmail.com',
             people_name='eee',
             people_phone='0974568934',
             people_birthday='1998-1-1',
             people_password='eee123'
             )

admin = People(people_email='admin@gmail.com',
               people_name='Marinka',
               people_phone='0660336265',
               people_birthday='2000-10-17',
               people_password='admin')

food_fest = Fest(fest_name='food_fest',
           people_email='ddd@gmail.com',
           fest_date='2021-1-4')

musical_fest = Fest(fest_name='musical_fest',
                  people_email='bbb@gmail.com',
                  fest_date='2021-3-8'
                  )

math_fest = Fest(fest_name='math_fest',
                 people_email='aaa@gmail.com',
                 fest_date='2021-12-2'
                 )

animal_fest = Fest(fest_name='animal_fest',
                    people_email='ddd@gmail.com',
                    fest_date='2021-10-29'
                    )

football_fest = Fest(fest_name='football_fest',
                 people_email='ddd@gmail.com',
                 fest_date='2021-1-1'
                 )

restaurant = Place(place_name='restaurant ',
                   place_adress='Soborna 23',
                   place_price=100
                   )

club = Place(place_name='club',
             place_adress='Solomianka 24',
             place_price=300
             )

library = Place(place_name='library',
                place_adress='Sosnova 56',
                place_price=0
                )

zoo = Place(place_name='zoo',
            place_adress='Nagirna 34',
            place_price=500
            )

stadium = Place(place_name='stadium',
                place_adress='Shiklna 9',
                place_price=200
                )

ddd.people_fest.append(food_fest)
bbb.people_fest.append(musical_fest)
aaa.people_fest.append(math_fest)
ddd.people_fest.append(animal_fest)
ddd.people_fest.append(football_fest)


food_fest.place_name_fk.append(restaurant)
musical_fest.place_name_fk.append(club)
math_fest.place_name_fk.append(library)
animal_fest.place_name_fk.append(zoo)
football_fest.place_name_fk.append(stadium)


db.session.add_all([aaa, bbb, ccc, ddd, eee, admin,
                    food_fest, musical_fest, math_fest, animal_fest, football_fest,
                    restaurant, club, library, zoo, stadium,
                    ])

db.session.commit()


def dropSession():
    session['people_email'] = ''
    session['role'] = 'unlogged'


def newSession(email, pw):
    session['people_email'] = email
    if pw == 'admin':
        session['role'] = 'admin'
    else:
        session['role'] = 'people_email'


@app.route('/')
def root():
    try:
        if not session['people_email']:
            return redirect('/login')
    except:
        session['people_email'] = ''
        session['role'] = 'unlogged'
        return redirect('/login')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate():
            try:
                res = db.session.query(People).filter(People.people_email == form.people_email.data).one()
            except:
                form.people_email.errors = ['This person has no account']
                return render_template('login.html', form=form)
            if res.people_password == form.people_password.data:
                newSession(res.people_email, res.people_password)
                return redirect('/')
            else:
                form.people_password.errors = ['Wrong password']
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    dropSession()
    return redirect('/login')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate():
            try:
                new_people = People(
                    people_email=form.people_email.data,
                    people_password=form.people_confirm_password.data
                )
                db.session.add(new_people)
                db.session.commit()
                newSession(new_people.people_email, new_people.people_password)
                return render_template('success.html')
            except:
                form.people_email.errors = ['This user is registered']
                return render_template('registration.html', form=form)
        else:
            return render_template('registration.html', form=form)

    return render_template('registration.html', form=form)


@app.route('/infouser', methods=['GET', 'POST'])
def user_info():
    result = db.session.query(People).all()
    return render_template('infouser.html', result=result)


@app.route('/edit_user/<string:email>', methods=['GET', 'POST'])
def edit_user(email):
    form = PeopleFormEdit()
    result = db.session.query(People).filter(People.people_email == email).one()

    if request.method == 'GET':

        form.people_name.data = result.people_name
        form.people_email.data = result.people_email
        form.people_birthday.data = result.people_birthday
        form.people_phone.data = result.people_phone

        return render_template('edit_user.html', form=form, form_name=email)
    elif request.method == 'POST':
        if form.validate() and form.validate_birthday():
            result.people_name = form.people_name.data
            result.user_email = form.people_email.data
            result.people_birthday = form.people_birthday.data.strftime("%Y-%m-%d")
            result.people_phone = form.people_phone.data

            db.session.commit()
            return redirect('/infouser')
        else:
            if not form.validate_birthday():
                form.people_birthday.errors = ['Year should be > 1900']
            return render_template('edit_user.html', form=form)


@app.route('/people')
def users():
    if session['role'] == 'admin':
        result = db.session.query(People).all()
        return render_template('all_people.html', result=result)
    else:
        return redirect('/login')


@app.route('/people/<string:email>')
def poeple_info(email):
    if session['role'] != 'unlogged':
        res = db.session.query(People).filter(People.people_email == email).one()
        return render_template('people_info.html', people=res)
    else:
        return redirect('/login')


@app.route('/edit_people/<string:email>', methods=['GET', 'POST'])
def edit_people(email):
    form = PeopleFormEdit()
    result = db.session.query(People).filter(People.people_email == email).one()

    if request.method == 'GET':

        form.people_name.data = result.people_name
        form.people_email.data = result.people_email
        form.people_birthday.data = result.people_birthday
        form.people_phone.data = result.people_phone

        return render_template('edit_people.html', form=form, form_name=email)

    elif request.method == 'POST':
        if form.validate() and form.validate_birthday():
            result.people_name = form.people_name.data
            result.user_email = form.people_email.data
            result.people_birthday = form.people_birthday.data.strftime("%Y-%m-%d")
            result.people_phone = form.people_phone.data

            db.session.commit()
            return redirect('/people')
        else:
            if not form.validate_birthday():
                form.people_birthday.errors = ['Year should be >1900']
            return render_template('edit_people.html', form=form)


@app.route('/edit_fest/<string:name>', methods=['GET', 'POST'])
def edit_fest(name):
    form = FestFormEdit()
    result = db.session.query(Fest).filter(Fest.fest_name == name).one()

    if request.method == 'GET':

        form.fest_name.data = result.fest_name
        form.fest_date.data = result.fest_date

        return render_template('edit_fest.html', form=form, form_name=name)

    elif request.method == 'POST':
        if form.validate() and form.validate_date():

            result.fest_name = form.fest_name.data
            result.fest_date = form.fest_date.data.strftime("%Y-%m-%d")

            db.session.commit()
            return redirect('/fest')
        else:
            if not form.validate_date():
                form.fest_date.errors = ['Year should be > 2020']
            return render_template('edit_fest.html', form=form)


@app.route('/delete_people/<string:email>', methods=['GET', 'POST'])
def delete_people(email):
    result = db.session.query(People).filter(People.people_email == email).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/people')


@app.route('/fest', methods=['GET'])
def all_fest():

    query = db.session.query(Fest.fest_name, Fest.fest_date, Fest.people_email, Place.place_name, Place.place_price, Place.place_adress)
    query = query.join(association, association.left_name == Fest.fest_name)
    query = query.join(Place, association.right_name == Place.place_name)
    result = query.all()

    return render_template('all_fest.html', result=result)


@app.route('/create_fest', methods=['POST', 'GET'])
def create_fest():
    form = FestForm()
    try:
        result = db.session.query(Fest).filter(Fest.fest_name == form.fest_name.data).one()
        if result != 0:
            return render_template('create_fest.html', fest_name="Fest already exists", form=form)
    except:
        pass
    if request.method == 'POST':
        if form.validate() and form.validate_date():
            new_fest = Fest(
                fest_name=form.fest_name.data,
                fest_date=form.fest_date.data.strftime("%Y-%m-%d"),
                people_email=form.people_email.data
            )
            new_place = Place(
                place_name=form.place_name.data,
                place_adress=form.place_adress.data,
                place_price=form.place_price.data
            )
            new_assosiation = association(
                left_name=form.fest_name.data,
                right_name=form.place_name.data,
            )
            db.session.add(new_fest)
            db.session.add(new_place)
            db.session.commit()
            db.session.add(new_assosiation)
            db.session.commit()
            return redirect('/fest')
        else:
            if not form.validate_date():
                form.fest_date.errors = ['Year should be > 2020']
            return render_template('create_fest.html', form=form)
    elif request.method == 'GET':
        return render_template('create_fest.html', form=form)


@app.route('/delete_fest/<string:name>', methods=['GET', 'POST'])
def delete_fest(name):
    result = db.session.query(Fest).filter(Fest.fest_name == name).one()

    db.session.delete(result)
    db.session.commit()

    return redirect('/fest')


@app.route('/place', methods=['GET'])
def all_place():
    result = db.session.query(Place).all()

    return render_template('all_place.html', result=result)


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    query = db.session.query(Fest.fest_name, Fest.fest_date, Place.place_name, Place.place_price, Place.place_adress)
    query = query.join(association, association.left_name == Fest.fest_name)
    query = query.join(Place, association.right_name == Place.place_name)

    if request.method == 'POST':
        if form.type_field.data == 'fest_name':
            res = query.filter(Fest.fest_name == form.search_value.data).all()
        elif form.type_field.data == 'fest_date':
            res = query.filter(Fest.fest_date == form.search_value.data).all()
        elif form.type_field.data == 'place_name':
            res = query.filter(Place.place_name == form.search_value.data).all()

        return render_template('search_result.html', vacancies=res)
    else:
        return render_template('search.html', form=form)


if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
