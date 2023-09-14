from datetime import datetime
from Model.match import Match


class Round:
    def __init__(self):
        self.nom = 1
        self.matchs = []
        self.date_debut = datetime.now()  # Initialisation automatique à l'instant actuel
        self.date_fin = None

    def end_turn(self):  # Correction du nom de la méthode
        self.date_fin = datetime.now()

    def to_dict(self):
        return {
            'nom': self.nom,
            'matchs': [match.to_dict() for match in self.matchs],
            'date_debut': self.date_debut.strftime('%Y-%m-%d %H:%M:%S'),
            'date_fin': self.date_fin.strftime('%Y-%m-%d %H:%M:%S') if self.date_fin else None
        }

    @classmethod
    def from_dict(cls, data):
        round_ = cls()
        round_.nom = data['nom']
        round_.matchs = [Match.from_dict(match_data) for match_data in data['matchs']]
        round_.date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%d %H:%M:%S')
        round_.date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%d %H:%M:%S') if data['date_fin'] else None

        return round_

