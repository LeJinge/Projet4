class Match:
    def __init__(self, joueur1, joueur2):
        self.joueur1 = [joueur1, 0]  # Joueur, Score
        self.joueur2 = [joueur2, 0]

    def set_score(self, score1, score2):
        self.joueur1[1] = score1
        self.joueur2[1] = score2
