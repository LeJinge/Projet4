from datetime import datetime

class Tour:
    def __init__(self, nom):
        self.nom = nom
        self.date_debut = datetime.now()
        self.date_fin = None
        self.matchs = []

    def tour_termine(self):
        self.date_fin = datetime.now()