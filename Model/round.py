from datetime import datetime


class Round:
    def __init__(self):
        self.nom = 0
        self.matchs = []
        self.date_debut = datetime.now()  # Initialisation automatique à l'instant actuel
        self.date_fin = None

    def end_turn(self):  # Correction du nom de la méthode
        self.date_fin = datetime.now()

    # Si vous souhaitez ajouter une méthode pour commencer le tour explicitement (optionnel) :
    def start_turn(self):
        self.date_debut = datetime.now()
