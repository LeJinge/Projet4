class Player:

    def __init__(self, last_name=None, first_name=None, birth_date=None, chess_id=None):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.score = 0  # initialisation du score à 0 par défaut
        self.previous_opponents = []  # initialisation de la liste des adversaires précédents vide par défaut

    @classmethod
    def from_dict(cls, data):
        player = cls()
        player.last_name = data.get("last_name")
        player.first_name = data.get("first_name")
        player.birth_date = data.get("birth_date")
        player.chess_id = data.get("chess_id")
        player.score = data.get("score", 0)  # Si "score" n'est pas dans data, initialisez à 0 par défaut
        player.previous_opponents = data.get("previous_opponents", [])  # Si "previous_opponents" n'est pas dans data, initialisez à une liste vide par défaut

        return player

    def to_dict(self):
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "chess_id": self.chess_id,
            "score": self.score,
            "previous_opponents": self.previous_opponents
        }
