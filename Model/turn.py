from datetime import datetime

class Tour:
    def __init__(self, last_name):
        self.last_name = last_name
        self.date_debut = datetime.now()
        self.date_fin = None
        self.matchs = []

    def tour_termine(self):
        self.date_fin = datetime.now()