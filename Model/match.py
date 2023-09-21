from Model.player import Player


class Match:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.completed = False
        self.score_player1 = 0
        self.score_player2 = 0

    def set_score(self, score1, score2):
        self.score_player1 = score1
        self.score_player2 = score2

    @classmethod
    def from_dict(cls, data):
        player1 = Player.from_dict(data["player1"])
        player2 = Player.from_dict(data["player2"])
        match_obj = cls(player1, player2)
        match_obj.score_player1 = data.get("score_player1", 0)
        match_obj.score_player2 = data.get("score_player2", 0)
        match_obj.completed = data.get("completed", False)
        return match_obj

    def to_dict(self):
        return {
            'player1': self.player1.to_dict(),
            'player2': self.player2.to_dict(),
            'score_player1': self.score_player1,
            'score_player2': self.score_player2,
            'completed': self.completed  # Ajouté
        }

    def winner(self):
        if self.score_player1 > self.score_player2:
            return self.player1
        elif self.score_player1 < self.score_player2:
            return self.player2
        else:
            return None