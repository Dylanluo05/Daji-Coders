from __init__ import db
from create_task.foodModel import foods
import random


# this is method called by frontend, it has been randomized between Alchemy and Native SQL for fun
def foods_all():

    table = foods_all_sql()

    return table


# SQLAlchemy extract all users from database
def foods_all_alc():
    table = foods.query.all()
    json_ready = [food.read() for food in table]
    return json_ready


# Native SQL extract all users from database
def foods_all_sql():
    table = db.session.execute('select * from foods')
    json_ready = sqlquery_2_list(table)
    return json_ready


# SQLAlchemy extract users from database matching term
def foods_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = foods.query.order_by(foods.restaurantName).filter((foods.restaurantName.ilike(term)) | (foods.foodName.ilike(term)))
    return [food.read() for food in table]


# SQLAlchemy extract single user from database matching ID
def restaurant_by_id(restaurantID):
    """finds User in table matching userid """
    return foods.query.filter_by(restaurantID=restaurantID).first()


# SQLAlchemy extract single user from database matching email
def restaurant_by_food(foodName):
    """finds User in table matching email """
    return foods.query.filter_by(foodName=foodName).first()


# ALGORITHM to convert the results of an SQL Query to a JSON ready format in Python
def sqlquery_2_list(rows):
    out_list = []
    keys = rows.keys()  # "Keys" are the columns of the sql query
    for values in rows:  # "Values" are rows within the SQL database
        row_dictionary = {}
        for i in range(len(keys)):  # This loop lines up K, V pairs, same as JSON style
            row_dictionary[keys[i]] = values[i]
        row_dictionary["query"] = "by_sql"  # This is for fun a little watermark
        out_list.append(row_dictionary)  # Finally we have a out_list row
    return out_list


# Test queries
if __name__ == "__main__":
    for i in range(10):
        print(foods_all())
