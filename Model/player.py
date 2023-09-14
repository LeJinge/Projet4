class Player:
    def __init__(self, last_name, first_name, birth_date, chess_id):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.score = 0  # ajout de l'attribut score
        self.previous_opponents = []  # ajout de l'attribut pour suivre les adversaires précédents

    def to_dict(self):
        return {
            'chess_id': self.chess_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'score': self.score
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(
            last_name=data['last_name'],
            first_name=data['first_name'],
            birth_date=data['birth_date'],
            chess_id=data['chess_id']
        )

        return player
