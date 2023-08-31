from tinydb import TinyDB, Query
from Model.player import Player
from Model.tournament import Tournament
from View.views import Views
from tinydb.storages import JSONStorage


class Menu:

    def __init__(self):
        self.player_admin = None
        self.tournament_admin = None

    def set_player_admin(self, gestion_joueurs):
        self.player_admin = gestion_joueurs

    def set_tournament_admin(self, tournament_admin):
        self.tournament_admin = tournament_admin

    @property
    def get_principal_menu_choice(self):

        principal_menu_choice = input("Veuillez faire un choix : ")
        return principal_menu_choice

    def display_principal_menu(self):

        while True:
            Views.view_principal_menu()
            principal_menu_choice = self.get_principal_menu_choice

            if principal_menu_choice == "1":
                if self.player_admin:
                    self.player_admin.get_user_choice_player()
                else:
                    print("Erreur: La gestion des joueurs n'est pas configurée.")
            elif principal_menu_choice == "2":
                if self.tournament_admin:
                    self.tournament_admin.get_user_choice_tournament()
                else:
                    print("Erreur: La gestion des tournois n'est pas configurée.")
            elif principal_menu_choice == "3":
                print("Au revoir!")
                break
            else:
                print("Choix non reconnu. Veuillez choisir une option valide.")


class PlayerController:

    def __init__(self):
        self.db_players = TinyDB('players.json', storage=JSONStorage, encoding='utf-8')
        self.table_players = self.db_players.table('players')
        self.PlayerView = Views()
        self.PlayerQuery = Query()

    def player_exist(self, chess_id):
        return bool(self.db_players.get(self.PlayerQuery.chess_id == chess_id))

    def add_player(self, player):

        if self.player_exist(player.chess_id):
            Views.message_player_duplicate()
        else:
            try:
                self.db_players.insert({
                    'chess_id': player.chess_id,
                    'last_name': player.last_name,
                    'first_name': player.first_name,
                    'birth_date': player.birth_date
                })

            except Exception as e:
                print("Erreur lors de l'insertion:", e)

    def get_user_choice_player(self):

        self.PlayerView.view_player_menu()
        choix = input("Veuillez faire un choix : ")

        if choix == "1":
            new_player = self.create_player()
            self.add_player(new_player)
        elif choix == "2":
            self.delete_player()
        elif choix == "3":
            self.update_player()
        elif choix == "4":
            return
        else:
            Views.message_non_valid_choice()

    def create_player(self):
        chess_id = input("Entrez l'Identifiant National d'échec du joueur : ")
        first_name = input("Entrez le prénom du joueur : ")
        last_name = input("Entrez le nom du joueur : ")
        birth_date = input("Entrez la date de naissance du joueur : ")

        new_player = Player(last_name, first_name, birth_date, chess_id)
        return new_player

    def delete_player(self):
        nom_a_effacer = input("Entrez le nom du joueur à effacer : ")
        prenom_a_effacer = input("Entrez le prénom du joueur à effacer : ")
        identifiant_a_effacer = input("Entrez l'Identifiant National d'échec du joueur à effacer : ")

        removed_count = self.db_players.remove(
            (self.PlayerQuery.last_name == nom_a_effacer) &
            (self.PlayerQuery.first_name == prenom_a_effacer) &
            (self.PlayerQuery.chess_id == identifiant_a_effacer)
        )

        if removed_count:
            Views.message_delete_player()
        else:
            Views.message_player_not_found()

    def update_player(self):
        chess_id = input("Entrez l'Identifiant National d'échec du joueur que vous souhaitez modifier : ")
        last_name = input("Entrez le nom du joueur que vous souhaitez modifier : ")
        first_name = input("Entrez le prénom du joueur que vous souhaitez modifier : ")

        player_found = self.db_players.get(
            (self.PlayerQuery.chess_id == chess_id) &
            (self.PlayerQuery.last_name == last_name) &
            (self.PlayerQuery.first_name == first_name)
        )

        if not player_found:
            Views.message_player_not_found()
            return

        print("Entrez les nouvelles informations pour le joueur:")
        new_last_name = input("Nom : ")
        new_first_name = input("Prénom : ")
        new_birth_date = input("Date de naissance (format YYYY-MM-DD) : ")
        new_chess_id = input("Nouvel Identifiant National d'échec : ")

        self.db_players.update({
            "last_name": new_last_name,
            "first_name": new_first_name,
            "birth_date": new_birth_date,
            "chess_id": new_chess_id
        }, (self.PlayerQuery.last_name == last_name) & (self.PlayerQuery.first_name == first_name) & (
                self.PlayerQuery.chess_id == chess_id))

        Views.message_modifie_player()

    def recover_player(self, last_name=None, first_name=None, chess_id=None):

        # Recherche par identifiant
        if chess_id:
            joueur_dict = self.db_players.get(self.PlayerQuery.chess_id == chess_id)

        # Recherche par nom et prénom
        elif last_name & first_name:
            joueur_dict = self.db_players.get(
                (self.PlayerQuery.last_name == last_name) & (self.PlayerQuery.first_name == first_name))

        if joueur_dict:
            # Convertir le dictionnaire en un objet Joueur
            return Player(
                joueur_dict['last_name'],
                joueur_dict['first_name'],
                joueur_dict['birth_date'],
                joueur_dict.get('chess_id', None)
            )
        else:
            return None


class TournamentController:
    def __init__(self):
        self.db_tournament = TinyDB('tournament.json', storage=JSONStorage, encoding='utf-8')
        self.db_players = TinyDB('players.json', storage=JSONStorage, encoding='utf-8')
        self.tournament = []
        self.TournamentQuery = Query()
        self.display_player = PlayerController()
        self.tournament_view = Views()
        self.PlayerQuery = Query()

    def create_tournament(self):
        new_tournament = Tournament(self)

        new_tournament.name = input("Nom du tournoi : ")
        new_tournament.place = input("Lieu : ")
        new_tournament.start_date = input("Date de début : ")
        new_tournament.end_date = input("Date de fin : ")
        new_tournament.tours_numbers = int(input("Nombre de tours : "))

        for l in range(new_tournament.tours_numbers * 2):

            new_player = PlayerController.create_player(self)
            new_tournament.list_player_save.append(new_player)
            existing_player = self.db_players.get(self.PlayerQuery.chess_id == new_player.chess_id)
            if new_player.chess_id != (existing_player['chess_id'] if existing_player else None):
                self.db_players.insert(
                    {
                        "chess_id": new_player.chess_id,
                        "last_name": new_player.last_name,
                        "first_name": new_player.first_name,
                        "birth_date": new_player.birth_date
                    })
            else:
                pass
        serialized_players = [player.to_dict() for player in new_tournament.list_player_save]

        self.db_tournament.insert(
            {
                "name": new_tournament.name,
                "place": new_tournament.place,
                "start_date": new_tournament.start_date,
                "end_date": new_tournament.end_date,
                "tours_numbers": new_tournament.tours_numbers,
                "list_player_save": serialized_players
            }
        )

    def modifie_tournament(self):
        name_modifie_tournament = input("Entrez le nom du tournoi : ")

        tournament_found = self.db_tournament.get(
            (self.TournamentQuery.name == name_modifie_tournament)
        )

        if not tournament_found:
            Views.message_tournament_not_found()
            return

        print("Entrez les nouvelles informations pour le tournoi:")
        new_name = input("Nom : ")
        new_place = input("Lieu : ")
        new_start_date = input("Date de début : ")
        new_end_date = input("Date de fin : ")
        new_tours_numbers = int(input("Nombre de tour : "))
        new_list_player_save = []

        for l in range(new_tours_numbers * 2):

            new_player = PlayerController.create_player(self)
            new_list_player_save.append(new_player)
            existing_player = self.db_players.get(self.PlayerQuery.chess_id == new_player.chess_id)
            if new_player.chess_id != (existing_player['chess_id'] if existing_player else None):
                self.db_players.insert(
                    {
                        "chess_id": new_player.chess_id,
                        "last_name": new_player.last_name,
                        "first_name": new_player.first_name,
                        "birth_date": new_player.birth_date
                    })
            else:
                pass
        serialized_players = [player.to_dict() for player in new_list_player_save]

        self.db_tournament.update({
            "name": new_name,
            "place": new_place,
            "start_date": new_start_date,
            "end_date": new_end_date,
            "tours_numbers": new_tours_numbers,
            "list_player_save": serialized_players
        })

        Views.message_modifie_tournament()

    # def delete_tournament(self):

    # def continue_create_tournament(self):

    # def start_tournament(self):

    def get_user_choice_tournament(self):

        self.tournament_view.view_tournament_menu()
        tournament_menu_choice = input("Veuillez faire un choix : ")

        if tournament_menu_choice == "1":
            self.create_tournament()
        if tournament_menu_choice == "2":
            self.modifie_tournament()
        if tournament_menu_choice == "3":
            self.delete_tournament()
        if tournament_menu_choice == "4":
            self.continue_create_tournament()
        if tournament_menu_choice == "5":
            self.start_tournament()
        if tournament_menu_choice == "6":
            return
        else:
            Views.message_non_valid_choice()
