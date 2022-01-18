from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate

from __init__ import db, app

dbURI = 'sqlite:///model/websiteDB.db'
# Setup properties for the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
app.config['SECRET_KEY'] = 'SECRET_KEY'
# Create SQLAlchemy engine to support SQLite dialect (sqlite:)
db = SQLAlchemy(app)
Migrate(app, db)


class webPages(db.Model):
    pageID = db.Column(db.Integer, primary_key=True)
    pageName = db.Column(db.String(255), unique=False, nullable=False)
    pageURL = db.Column(db.String(255), unique=True, nullable=False)
    pageDesc = db.Column(db.String(255), unique=False, nullable=False)


    def __init__(self, pageName, pageURL, pageDesc):
        self.pageName = pageName
        self.pageURL = pageURL
        self.pageDesc = pageDesc

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
            "pageID": self.pageID,
            "pageName": self.pageName,
            "pageURL": self.pageURL,
            "pageDesc": self.pageDesc
        }


    def update(self, pageName, pageURL='', pageDesc=''):
        if len(pageName) > 0:
            self.pageName = pageName
        if len(pageURL) > 0:
            self.pageURL = pageURL
        if len(pageDesc) > 0:
            self.pageDesc = pageDesc
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


def model_tester():
    db.create_all()
    p1 = webPages(pageName='Fun Times', pageURL='http://127.0.0.1:8000/FunTimes/', pageDesc='Fun Times for fun people :)')
    p2 = webPages(pageName='Hotel Search', pageURL='http://127.0.0.1:8000/HotelSearch/', pageDesc='Find a hotel for your next vacation here!')
    p3 = webPages(pageName='Car Rental', pageURL='http://127.0.0.1:8000/CarSearch/', pageDesc='Rent a car here!')
    p4 = webPages(pageName='Foodie Finder', pageURL='http://127.0.0.1:8000/RestaurantSearch/', pageDesc='Require sustenance during your trip? FInd somewhere to eat here!')
    p5 = webPages(pageName='Currency Exchange', pageURL='http://127.0.0.1:8000/currency_exchange/', pageDesc='Learn how much your money is worth in another country')
    table = [p1, p2, p3, p4, p5]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print(f"Records already exist: {row.pageURL}")


def model_printer():
    print("------------")
    print("Table: webPages with SQL query")
    print("------------")
    #result = db.session.execute('select * from webpages')
    #print(result.keys())
    result = webPages.query.all()
    json_ready = [page.read() for page in result]
    for row in json_ready:
        print(row)


if __name__ == "__main__":
    model_tester()  # builds model of Users
    model_printer()