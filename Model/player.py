class Player:

    def __init__(self,
                 last_name=None,
                 first_name=None,
                 birth_date=None,
                 chess_id=None):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.chess_id = chess_id
        self.score = 0
        self.previous_opponents = []

    @classmethod
    def from_dict(cls, data):
        if not all(
                key in data for key in ["last_name",
                                        "first_name",
                                        "birth_date",
                                        "chess_id"]):
            raise ValueError("Missing data to instantiate Player")

        player = cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birth_date=data["birth_date"],
            chess_id=data["chess_id"]
        )
        player.score = data.get("score", 0)
        player.previous_opponents = data.get("previous_opponents", [])
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
