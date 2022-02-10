from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from __init__ import db, app

dbURI = 'sqlite:///model/foodDB.db'
# Setup properties for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
# Create SQLAlchemy engine to support SQLite dialect (sqlite:)
db = SQLAlchemy(app)
Migrate(app, db)


class foods(db.Model):
    restaurantID = db.Column(db.Integer, primary_key=True)
    restaurantName = db.Column(db.String(255), unique=False, nullable=False)
    foodName = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, restaurantName, foodName):
        self.restaurantName = restaurantName
        self.foodName = foodName

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "restaurantName": self.restaurantName,
            "foodName": self.foodName,
        }

    def update(self, restaurantName, foodName=''):
        if len(restaurantName) > 0:
            self.restaurantName = restaurantName
        if len(foodName) > 0:
            self.foodName = foodName
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


def model_tester():
    db.create_all()
    f1 = foods(restaurantName='Chipotle', foodName='Burrito')
    f2 = foods(restaurantName='Outback Steakhouse', foodName='Steak')
    f3 = foods(restaurantName='California Pizza Kitchen', foodName='Pizza')
    f4 = foods(restaurantName='Olleh Korean Barbeque', foodName='BBQ')
    f5 = foods(restaurantName='Pho Ca Dao', foodName='Pho')
    f6 = foods(restaurantName='Buca', foodName='Pasta')
    table = [f1, f2, f3, f4, f5, f6]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print(f"Records already exist: {row.foodName}")


def model_printer():
    print("------------")
    print("Table: Resturants and iconic foods")
    print("------------")
    # result = db.session.execute('select * from webpages')
    # print(result.keys())
    result = foods.query.all()
    json_ready = [food.read() for food in result]
    for row in json_ready:
        print(row)


if __name__ == "__main__":
    model_tester()  # builds model of Users
    model_printer()
