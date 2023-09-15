from datetime import datetime
from Model.player import Player
from Model.match import Match


class Round:
    def __init__(self):
        self.name = 1
        self.matchs = []
        self.date_debut = datetime.now()  # Initialisation automatique à l'instant actuel
        self.date_fin = None

    def end_turn(self):  # Correction du nom de la méthode
        self.date_fin = datetime.now()

    def to_dict(self):
        return {
            'name': self.name,
            'matchs': [match.to_dict() for match in self.matchs],
            'date_debut': self.date_debut.strftime('%Y-%m-%d %H:%M:%S'),
            'date_fin': self.date_fin.strftime('%Y-%m-%d %H:%M:%S') if self.date_fin else None
        }

    @classmethod
    def from_dict(cls, data):
        round_obj = cls()
        round_obj.name = data.get('name')
        round_obj.date_debut = datetime.strptime(data.get('date_debut', ''), '%Y-%m-%d %H:%M:%S')
        round_obj.date_fin = datetime.strptime(data.get('date_fin', ''), '%Y-%m-%d %H:%M:%S') if data.get(
            'date_fin') else None
        round_obj.matchs = [Match.from_dict(match_data) for match_data in data.get('matchs', [])]
        return round_obj

