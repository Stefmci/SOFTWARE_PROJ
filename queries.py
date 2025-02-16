import os
from tinydb import TinyDB, Query
from serializer import serializer

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')
db = TinyDB(db_path, storage=serializer) 

def save_points(id, x, y, fixed=False):
    points_table = db.table('points')
    points_query = Query()
    points_table.upsert({'id': id, 'x': x, 'y': y, 'fixed': fixed}, points_query.id == id)

def get_all_points():
    points_table = db.table('points')
    return points_table.all()

def delete_points(id):
    points_table = db.table("points")
    points_query = Query()
    points_table.remove(points_query.id == id)

def find_points() -> list:
    points_table = db.table("points")
    result = points_table.all()
    return [x.get("id", "Unbekannt") for x in result] if result else []

def delete_all_points():
    points_table = db.table("points")
    points_table.truncate()  
