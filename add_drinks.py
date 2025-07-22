from app import app
from models import db, Drink

boissons = [
    Drink(name="Bière", alcohol_percentage=5, volume_ml=250, category="Bière"),
    Drink(name="Vin rouge", alcohol_percentage=12, volume_ml=120, category="Vin"),
    Drink(name="Vodka", alcohol_percentage=40, volume_ml=40, category="Spiritueux"),
    Drink(name="Whisky", alcohol_percentage=40, volume_ml=40, category="Spiritueux"),
    Drink(name="Champagne", alcohol_percentage=12, volume_ml=100, category="Vin"),
]

with app.app_context():
    db.session.add_all(boissons)
    db.session.commit()
    print("Boissons ajoutées !") 