from tinydb import TinyDB, Query
from Model.player import Player
from Model.tournament import Tournament
from View.views import Views
from tinydb.storages import JSONStorage


class Menu:

    def __init__(self):
        self.gestion_joueurs = None
        self.gestion_tournoi = None

    def set_gestion_joueurs(self, gestion_joueurs):
        self.gestion_joueurs = gestion_joueurs

    def set_gestion_tournoi(self, gestion_tournoi):
        self.gestion_tournoi = gestion_tournoi

    @property
    def get_principal_menu_choice(self):

        principal_menu_choice = input("Veuillez faire un choix : ")
        return principal_menu_choice

    def display_principal_menu(self):

        while True:
            Views.view_principal_menu()
            principal_menu_choice = self.get_principal_menu_choice

            if principal_menu_choice == "1":
                if self.gestion_joueurs:
                    self.gestion_joueurs.get_user_choice()
                else:
                    print("Erreur: La gestion des joueurs n'est pas configurée.")
            elif principal_menu_choice == "2":
                if self.gestion_tournoi:
                    self.gerer_tournois()
                else:
                    print("Erreur: La gestion des tournois n'est pas configurée.")
            elif principal_menu_choice == "3":
                print("Au revoir!")
                break
            else:
                print("Choix non reconnu. Veuillez choisir une option valide.")


class PlayerController:

    def __init__(self):
        self.db = TinyDB('players.json', storage=JSONStorage, encoding='utf-8')
        self.table_players = self.db.table('players')
        self.PlayerView = Views()
        self.PlayerQuery = Query()

    def player_exist(self, chess_id):
        return bool(self.db.get(self.PlayerQuery.chess_id == chess_id))

    def add_player(self, player):

        if self.player_exist(player.chess_id):
            Views.message_player_duplicate()
        else:
            try:
                self.db.insert({
                    'chess_id': player.chess_id,
                    'last_name': player.last_name,
                    'first_name': player.first_name,
                    'birth_date': player.birth_date
                })

            except Exception as e:
                print("Erreur lors de l'insertion:", e)

    def get_user_choice(self):

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

        removed_count = self.db.remove(
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

        player_found = self.db.get(
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

        self.db.update({
            "last_name": new_last_name,
            "first_name": new_first_name,
            "birth_date": new_birth_date,
            "chess_id": new_chess_id
        }, (self.PlayerQuery.last_name == last_name) & (self.PlayerQuery.first_name == first_name) & (
                self.PlayerQuery.chess_id == chess_id))

        Views.message_modifie_player()

    class TournamentController:
        def __init__(self):
            self.db = TinyDB('tournament.json')
            self.tournament = []
            self.display_player = PlayerController()
            self.tournament_view = Views.view_tournament_menu()


