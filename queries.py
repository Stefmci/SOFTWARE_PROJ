import os
from tinydb import TinyDB, Query
from serializer import serializer
from classes import Mechanismus

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')
db = TinyDB(db_path, storage=serializer) 


def save_mechanismus(mechanismus: Mechanismus, force=False):
    mechanisms_table = db.table("mechanisms")
    query = Query()
    mechanisms_table.upsert(mechanismus.to_dict(), query.id == mechanismus.id)
    if existing and not force:
        print(f"Mechanismus mit ID '{mechanismus.id}' existiert bereits! Aktualisiere den Eintrag.")
    mechanisms_table.upsert(mechanismus.to_dict(), query.id == mechanismus.id)
    print(f"Mechanismus '{mechanismus.id}' wurde gespeichert (aktualisiert)!")


def load_mechanismus(id: str) -> Mechanismus:
    mechanisms_table = db.table("mechanisms")
    query = Query()
    result = mechanisms_table.get(query.id == id)
    if result:
        return Mechanismus.from_dict(result)
    else:
        print(f"Mechanismus mit ID '{id}' nicht gefunden.")
        return None


def get_all_mechanismen():
    mechanisms_table = db.table("mechanisms")
    return [m["id"] for m in mechanisms_table.all()]


def delete_mechanismus(id: str):
    mechanisms_table = db.table("mechanisms")
    query = Query()
    mechanism = load_mechanismus(id)
    mechanisms_table.remove(query.id == id)
    print(f"Mechanismus mit ID '{id}' wurde gelöscht.")


def update_mechanismus(id: str, neue_punkte=None, neue_stangen=None):
    mechanismus = load_mechanismus(id)
    if not mechanismus:
        print(f"Mechanismus mit ID '{id}' nicht gefunden.")
        return
    
    if neue_punkte:
        for p in neue_punkte:
            if p["id"] in mechanismus.punkte:
                mechanismus.punkte[p["id"]].set_position(p["x"], p["y"])
            else:
                mechanismus.add_point(p["id"], p["x"], p["y"], p.get("fixed", False))

    if neue_stangen:
        for s in neue_stangen:
            mechanismus.remove_link(s["p1"], s["p2"])
            mechanismus.add_link(s["p1"], s["p2"])

    save_mechanismus(mechanismus)
    print(f"Mechanismus '{id}' wurde aktualisiert.")


