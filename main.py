from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField, BooleanField
import DBConnection

SECRET_KEY = 'dev'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

db = DBConnection.Database()
cursor = db.cursor


@app.route('/', methods=['get', 'post'])
def homepage():
    class searchForm(FlaskForm):
        university = RadioField("University", choices=[('', 'All'), ('uoit', 'UOIT'), ('utsc', 'U of T - Scarborough'), ('utm', 'U of T - Mississauga')], default='')
        room = RadioField("RoomType", choices=[('', 'All'), ('furnished', 'Furnished'), ('unfurnished', 'Unfurnished')], default='')
        washroom = RadioField("Washroom", choices=[('', 'All'), ('separate', 'Separate'), ('shared', 'Shared')], default='')
        parking = BooleanField("Parking", validators=[])

    form = searchForm()

    if form.validate_on_submit():
        university = form.university.data
        room = form.room.data
        washroom = form.washroom.data
        parking = form.parking.data
        price = request.form['price']
        size = request.form['size']

        result = db.getListings(university, room, washroom, parking, price, size)

        print(result)

        return render_template('index.html', form=form, results=result)

    else:
        print(form.errors)

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
