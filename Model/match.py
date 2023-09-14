from Model.player import Player


class Match:
    def __init__(self, joueur1: Player, joueur2: Player):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score_joueur1 = 0
        self.score_joueur2 = 0

    def set_score(self, score1, score2):
        self.score_joueur1 = score1
        self.score_joueur2 = score2

    def to_dict(self):
        return {
            'joueur1': self.joueur1.to_dict(),
            'score_joueur1': self.score_joueur1,
            'joueur2': self.joueur2.to_dict(),
            'score_joueur2': self.score_joueur2
        }

    @classmethod
    def from_dict(cls, data):
        joueur1 = Player.from_dict(data['joueur1'])
        joueur2 = Player.from_dict(data['joueur2'])
        match_ = cls(joueur1=joueur1, joueur2=joueur2)
        match_.score_joueur1 = data['score_joueur1']
        match_.score_joueur2 = data['score_joueur2']

        return match_
