from typing import List
from Model.round import Round
from Model.player import Player


class Tournament:
    def __init__(self, name="", place="", start_date="", end_date="", rounds_numbers=4):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.rounds_numbers = rounds_numbers
        self.current_round = 1
        self.list_tours: List[Round] = []
        self.list_player_save: List[Player] = []
        self.description = ""

    @classmethod
    def from_dict(cls, data):
        if not all(key in data for key in ["name", "place", "start_date", "end_date", "rounds_numbers"]):
            raise ValueError("Missing data to instantiate Tournament")

        tournament = cls(
            name=data["name"],
            place=data["place"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            rounds_numbers=data["rounds_numbers"]
        )
        tournament.current_round = data.get("current_round", 1)
        tournament.list_tours = [Round.from_dict(tour_data) for tour_data in data.get("list_tours", [])]
        tournament.list_player_save = [Player.from_dict(player_data) for player_data in
                                       data.get("list_player_save", [])]
        tournament.description = data.get("description", "")
        return tournament

    def to_dict(self):
        return {
            "name": self.name,
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "rounds_numbers": self.rounds_numbers,
            "current_round": self.current_round,
            "list_tours": [round_obj.to_dict() for round_obj in self.list_tours],
            "list_player_save": [player.to_dict() for player in self.list_player_save],
            "description": self.description,
        }
