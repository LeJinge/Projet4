from Model.player import Player


class Match:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.score_player1 = 0
        self.score_player2 = 0

    def set_score(self, score1, score2):
        self.score_player1 = score1
        self.score_player2 = score2

    @classmethod
    def from_dict(cls, data):
        return Match(**data)

    def to_dict(self):
        return {
            'player1': self.player1.to_dict(),
            'player2': self.player2.to_dict(),
            'score_player1': self.score_player1,
            'score_player2': self.score_player2
        }

    def winner(self):
        if self.score_player1 > self.score_player2:
            return self.player1
        elif self.score_player1 < self.score_player2:
            return self.player2
        else:
            return None