class Tournament:
    def __init__(self, name="", place="", start_date="", end_date="", rounds_numbers=4, current_round= ""):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.rounds_numbers = rounds_numbers
        self.current_round = current_round
        self.list_tours = []
        self.list_player_save = []
        self.description = ""