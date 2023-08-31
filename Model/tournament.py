class Tournament:
    def __init__(self, name="", place="", start_date="", end_date="", tours_numbers=4, actual_tour= ""):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.tours_numbers = tours_numbers
        self.actual_tour = actual_tour
        self.list_tours = []
        self.list_player_save = []
        self.description = ""