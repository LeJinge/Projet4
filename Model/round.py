from datetime import datetime
from Model.match import Match


class Round:
    def __init__(self, name=None):
        self.name = name
        self.matchs = []
        self.date_debut = datetime.now()
        self.date_fin = None

    def end_turn(self):  # Correction du nom de la méthode
        self.date_fin = datetime.now()

    def to_dict(self):
        try:
            round_data = {
                "name": self.name,
                "date_debut": self.date_debut.strftime("%Y-%m-%d %H:%M:%S"),
                "date_fin": self.date_fin.strftime("%Y-%m-%d %H:%M:%S")
                if self.date_fin
                else None,
            }
            if len(self.matchs) > 0:
                round_data["matchs"] = [match.to_dict() for
                                        match in self.matchs]
            return round_data

        except AttributeError as e:
            raise ValueError(
                f"Failed to serialize the Round object: {e}"
            )

    @classmethod
    def from_dict(cls, data):
        try:
            # Valider les champs obligatoires
            if "name" not in data or "date_debut" not in data:
                raise ValueError(
                    "Missing necessary fields for deserialization."
                )

            # Créer une instance de Round
            round_obj = cls()
            round_obj.name = data["name"]
            round_obj.date_debut = datetime.strptime(
                data["date_debut"], "%Y-%m-%d %H:%M:%S"
            )

            # Vérifier si la date de fin est présente et la convertir
            if data.get("date_fin"):
                round_obj.date_fin = datetime.strptime(
                    data["date_fin"], "%Y-%m-%d %H:%M:%S")
            else:
                round_obj.date_fin = None

            # Valider et convertir les matchs
            match_data = data.get("matchs", [])
            if not isinstance(match_data, list):
                raise ValueError(
                    f"Expected 'matchs' to be a list, "
                    f"got {type(match_data).__name__} instead."
                )

            round_obj.matchs = [Match.from_dict(match) for match in match_data]

            return round_obj

        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Failed to deserialize the Round object from dict: {e}"
            )
