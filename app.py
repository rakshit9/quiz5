import pyodbc
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
import os
import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecureSecretKey'
db_table = "Earthquakes"


def connection():
    server = 'summer24.database.windows.net'
    username = 'rakshit'
    password = 'Canada@90'
    database = 'dk'
    driver = '{ODBC Driver 18 for SQL Server}'
    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    return conn


@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        conn = connection()
        cursor = conn.cursor()
        msg = "Database Connected Successfully"
        return render_template('index.html', error=msg)
    except Exception as e:
        return render_template('index.html', error=e)


class Form1(FlaskForm):
    mag = StringField(label='Enter Magnitude: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


def get_magnitude_data(cursor, mag1, mag2=None):
    if mag2:
        query = 'SELECT count(*) from {} where mag >= ? and mag < ?'.format(db_table)
        params = (mag1, mag2)
        label = f'Mag. between {mag1} to {mag2}'
    else:
        query = 'SELECT count(*) from {} where mag >= ?'.format(db_table)
        params = (mag1,)
        label = f'Mag. greater than {mag1}'

    cursor.execute(query, params)
    return label, cursor.fetchone()[0]



@app.route('/form1', methods=['GET', 'POST'])
def one():
    try:
        conn = connection()
        cursor = conn.cursor()
        cnt = 0
        result = {}
        magnitude_ranges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5,)]

        for mag_range in magnitude_ranges:
            label, mag_data = get_magnitude_data(cursor, *mag_range)
            result[label] = mag_data
            cnt += mag_data

        return render_template('form1.html', result=result, cnt=cnt, data=1)

    except Exception as e:
        print(e)
        return render_template('form1.html', error='Enter numeric value.')


class Two2(FlaskForm):
    d1 = StringField(label='Lower Range of Depth: ', validators=[DataRequired()])
    d2 = StringField(label='Upper Range of Depth: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route('/form2', methods=['GET', 'POST'])
def two():
    form = Two2()
    cnt = 0
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()
            d1 = float(form.d1.data)
            d2 = float(form.d2.data)

            if d1 > d2:
                return render_template('form2.html', form=form, error='Lower range must be lower then upper range.')

            cursor.execute('SELECT count(*) as "Mag. less then 1.0" from {} where mag < 1 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result = {columns[0]: row[0]}
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 1.0 to 2.0" from {} where mag >= 1.0 and  mag <2.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 2.0 to 3.0" from {} where mag >= 2.0 and mag < 3.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 3.0 to 4.0" from {} where mag >= 3.0 and mag < 4.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. between 4.0 to 5.0" from {} where mag >= 4.0 and mag < 5.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. grater then 5.0" from {} where mag >= 5.0 and depth between ? and ?'.format(db_table), d1, d2)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            return render_template('form2.html', result=result, cnt=cnt, data=1)

        except Exception as e:
            print(e)
            return render_template('form2.html', form=form, error='Enter numeric value.')

    return render_template('form2.html', form=form)


class Three3(FlaskForm):
    m1 = StringField(label='Lower Range of Magnitude: ', validators=[DataRequired()])
    m2 = StringField(label='Upper Range of Magnitude: ', validators=[DataRequired()])
    d1 = StringField(label='Lower Range of Depth: ', validators=[DataRequired()])
    d2 = StringField(label='Upper Range of Depth: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route('/form3', methods=['GET', 'POST'])
def three():
    form = Three3()
    cnt = 0
    if form.validate_on_submit():
        try:
            conn = connection()
            cursor = conn.cursor()
            m1 = float(form.m1.data)
            m2 = float(form.m2.data)
            d1 = float(form.d1.data)
            d2 = float(form.d2.data)

            if d1 > d2 or m1 > m2:
                return render_template('form3.html', form=form, error='Lower range must be lower then upper range.')

            result = dict()

            cursor.execute('select mag,depth from {} where mag BETWEEN ? and ? and depth BETWEEN ? and ? order by mag,depth'.format(db_table), m1, m2, d1, d2)
            for row in cursor.fetchall():
                for i in row:
                    result.setdefault(cnt, []).append(i)
                cnt += 1

            return render_template('form3.html', result=result, d1=d1, d2=d2, m1=m1, m2=m2, cnt=cnt, form=form, data=1)

        except Exception as e:
            print(e)
            return render_template('form3.html', form=form, error='Enter numeric value.')

    return render_template('form3.html', form=form)


@app.route('/form4', methods=['GET', 'POST'])
def four():
    cnt = 0
    if request.method == "POST":
        try:
            conn = connection()
            cursor = conn.cursor()
            clus = request.form['type']

            cursor.execute('SELECT count(*) as "Mag. less then 1.0" from {} where mag < 1 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result = {columns[0]: row[0]}
                cnt += row[0]

            cursor.execute(
                'SELECT count(*) as "Mag. between 1.0 to 2.0" from {} where mag >= 1.0 and  mag <2.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute(
                'SELECT count(*) as "Mag. between 2.0 to 3.0" from {} where mag >= 2.0 and mag < 3.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute(
                'SELECT count(*) as "Mag. between 3.0 to 4.0" from {} where mag >= 3.0 and mag < 4.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute(
                'SELECT count(*) as "Mag. between 4.0 to 5.0" from {} where mag >= 4.0 and mag < 5.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            cursor.execute('SELECT count(*) as "Mag. grater then 5.0" from {} where mag >= 5.0 and type = ?'.format(db_table), clus)
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                result[columns[0]] = row[0]
                cnt += row[0]

            return render_template('form4.html', result=result, type=clus, cnt=cnt, data=1)

        except Exception as e:
            print(e)
            return render_template('form4.html', error=e)

    return render_template('form4.html')



class FoodForm(FlaskForm):
    command = SelectField(label='Command:', choices=[('add', 'Add'), ('delete', 'Delete'), ('modify', 'Modify')], validators=[DataRequired()])
    food_name = StringField(label='Food Name:', validators=[DataRequired()])
    quantity = IntegerField(label='Quantity:', validators=[DataRequired()])
    price = IntegerField(label='Price:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/manage_food', methods=['GET', 'POST'])
def manage_food():
    form = FoodForm()
    result = None

    if form.validate_on_submit():
        command = form.command.data
        food_name = form.food_name.data
        quantity = form.quantity.data
        price = form.price.data

        try:
            conn = connection()
            cursor = conn.cursor()

            if command == 'add':
                cursor.execute('INSERT INTO food (food, quantity, price) VALUES (?, ?, ?)', (food_name, quantity, price))
            elif command == 'delete':
                cursor.execute('DELETE FROM food WHERE food = ?', (food_name,))
            elif command == 'modify':
                cursor.execute('UPDATE food SET quantity = ?, price = ? WHERE food = ?', (quantity, price, food_name))

            conn.commit()

            cursor.execute('SELECT * FROM food')
            result = cursor.fetchall()
        except Exception as e:
            return render_template('manage_food.html', form=form, error=str(e))

    return render_template('manage_food.html', form=form, result=result)

class TopNForm(FlaskForm):
    n_value = IntegerField(label='Enter N:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/top_n_food', methods=['GET', 'POST'])
def top_n_food():
    form = TopNForm()
    result = None

    if form.validate_on_submit():
        n_value = form.n_value.data

        try:
            conn = connection()
            cursor = conn.cursor()
            query = f'SELECT TOP {n_value} food, quantity FROM food ORDER BY quantity DESC'
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            return render_template('top_n_food.html', form=form, error=str(e))

    return render_template('top_n_food.html', form=form, result=result)

class TopNPriceForm(FlaskForm):
    n_value = IntegerField(label='Enter N:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/top_n_price_food', methods=['GET', 'POST'])
def top_n_price_food():
    form = TopNPriceForm()
    result = None

    if form.validate_on_submit():
        n_value = form.n_value.data

        try:
            conn = connection()
            cursor = conn.cursor()
            query = f'SELECT TOP {n_value} food, price FROM food ORDER BY price DESC'
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            return render_template('top_n_price_food.html', form=form, error=str(e))

    return render_template('top_n_price_food.html', form=form, result=result)

class AddPointForm(FlaskForm):
    x_value = IntegerField(label='X Value:', validators=[DataRequired()])
    y_value = IntegerField(label='Y Value:', validators=[DataRequired()])
    quantity = IntegerField(label='Quantity:', validators=[DataRequired()])
    submit = SubmitField(label='Add Point')

@app.route('/scatter_chart', methods=['GET', 'POST'])
def scatter_chart():
    form = AddPointForm()
    result = None

    if form.validate_on_submit():
        x_value = form.x_value.data
        y_value = form.y_value.data
        quantity = form.quantity.data

        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO points (x, y, quantity) VALUES (?, ?, ?)', (x_value, y_value, quantity))
            conn.commit()

            cursor.execute('SELECT x, y, quantity FROM points')
            result = cursor.fetchall()
        except Exception as e:
            return render_template('scatter_chart.html', form=form, error=str(e))

    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute('SELECT x, y, quantity FROM points')
            result = cursor.fetchall()
        except Exception as e:
            return render_template('scatter_chart.html', form=form, error=str(e))

    return render_template('scatter_chart.html', form=form, result=result)


if __name__ == "__main__":
    app.run(debug=True)