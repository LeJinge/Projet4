class Player:
    def __init__(self, last_name, first_name, birth_date=None, chess_id=None):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id

    def to_dict(self):
        return {
            'chess_id': self.chess_id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date
        }
