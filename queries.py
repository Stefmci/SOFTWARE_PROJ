import os
from tinydb import TinyDB, Query
from serializer import serializer
from classes import Mechanism, Point

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')
db = TinyDB(db_path, storage=serializer)

def save_mechanism(mechanism: Mechanism, force=False):
    mechanisms_table = db.table("mechanisms")
    query = Query()
    existing = mechanisms_table.get(query.id == mechanism.id)
    if existing and not force:
        raise ValueError("Mechanism already exists! If you want to overwrite it, set force=True.")
    
    mechanisms_table.upsert(mechanism.to_dict(), query.id == mechanism.id)
    print(f"Mechanism '{mechanism.id}' has been saved (updated)!")

    return True #Hier musste ich (Ahmet) True zurückgeben für den Tracepunkt

def load_mechanism(id: str) -> Mechanism:
    mechanisms_table = db.table("mechanisms")
    query = Query()
    result = mechanisms_table.get(query.id == id)
    if result:
        return Mechanism.from_dict(result)
    else:
        print(f"Mechanism with ID '{id}' not found.")
        return None

def get_all_mechanisms():
    mechanisms_table = db.table("mechanisms")
    return [m["id"] for m in mechanisms_table.all()]

def delete_mechanism(id: str):
    mechanisms_table = db.table("mechanisms")
    query = Query()
    mechanism = load_mechanism(id)
    if mechanism:
        mechanisms_table.remove(query.id == id)
        print(f"Mechanism with ID '{id}' has been deleted.")
    else:
        print(f"Mechanism with ID '{id}' does not exist.")

def save_trace(mechanism_id: str, point_id: str):
    mech = load_mechanism(mechanism_id)
    if mech is None:
        print(f"Mechanismus '{mechanism_id}' nicht gefunden!")
        return

    # Den gewählten Punkt als Trace-Punkt setzen
    for point in mech.points:
        if point.id == point_id or point.name == point_id:
            point.trace_point = True
            print(f"Trace-Punkt für '{point_id}' gesetzt.")

            save_mechanism(mech, force=True)  # Daten speichern
            print("Mechanismus erfolgreich gespeichert!")  # <== Debugging
            return




