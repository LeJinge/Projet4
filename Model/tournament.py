class Tournament:
    def __init__(self, last_name, lieu, date_debut, date_fin, nombre_tours=4, tour_actuel= ""):
        self.last_name = last_name
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_tours = nombre_tours
        self.tour_actuel = tour_actuel
        self.liste_tours = []
        self.liste_joueurs_enregistres = []
        self.description = ""