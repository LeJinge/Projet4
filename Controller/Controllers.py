from tinydb import TinyDB, Query
from Model.player import Player
from Model.tournament import Tournament
from View.views import Views
from tinydb.storages import JSONStorage
import random


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
        new_tournament.rounds_numbers = int(input("Nombre de tours : "))

        for l in range(new_tournament.rounds_numbers * 2):

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
                "rounds_numbers": new_tournament.rounds_numbers,
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
        new_rounds_numbers = int(input("Nombre de tour : "))
        new_list_player_save = []

        for l in range(new_rounds_numbers * 2):

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
            "rounds_numbers": new_rounds_numbers,
            "list_player_save": serialized_players
        })

        Views.message_modifie_tournament()

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
            self.start_tournament()
        if tournament_menu_choice == "5":
            self.resume_tournament()
        if tournament_menu_choice == "6":
            return
        else:
            Views.message_non_valid_choice()

    def delete_tournament(self):
        name_of_tournament_to_delete = input("Entrez le nom du tournoi à supprimer: ")

        tournament_found = self.db_tournament.get(self.TournamentQuery.name == name_of_tournament_to_delete)

        if tournament_found:
            self.db_tournament.remove(self.TournamentQuery.name == name_of_tournament_to_delete)
            Views.message_tournament_deleted()
        else:
            Views.message_tournament_not_found()

    def get_tournament_by_name(self, name):
        return self.db_tournament.search(self.TournamentQuery.name == name)[0]

    def start_tournament(self):
        tournament_name = input("Entrez le nom du tournoi que vous voulez commencer: ")

        # Récupérer les données du tournoi par son nom
        tournament_data = self.get_tournament_by_name(tournament_name)
        number_of_rounds = tournament_data['rounds_numbers']

        current_round = tournament_data.get('current_round', 0)
        current_match = tournament_data.get('current_match', 0)

        # Récupérer tous les joueurs du tournoi à partir de la base de données.
        players_list = [Player.from_dict(data) for data in tournament_data['list_player_save']]

        for i in range(current_round, number_of_rounds):
            print(f"\nDébut du tour {i + 1}!")
            players_list.sort(key=lambda x: x.score, reverse=True)

            matches = self.generate_matches(players_list)

            # Commencer les matchs à partir du match sauvegardé
            for j, match in enumerate(matches[current_match:], start=current_match):
                print(f"{match[0].first_name} ({match[0].score}) vs {match[1].first_name} ({match[1].score})")

                while True:
                    winner_id = input(f"Qui est le vainqueur ? 1. {match[0].first_name} 2. {match[1].first_name} : ")

                    if winner_id == "1":
                        match[0].score += 1
                        break
                    elif winner_id == "2":
                        match[1].score += 1
                        break
                    else:
                        print("Choix non valide. Veuillez sélectionner le bon numéro.")

                # Sauvegarde après chaque match
                self.save_tournament(tournament_name, players_list, i + 1, j + 1)

                # Vérifiez si l'utilisateur veut arrêter après le match
                exit_choice = input("Voulez-vous quitter le tournoi? (Oui/Non): ").lower()
                if exit_choice == 'oui':
                    return

            print(f"Fin du tour {i + 1}!\n")

            # Réinitialiser l'index du match pour le prochain tour
            current_match = 0

    def generate_matches(self, players_list):
        # Étape 1 : Trier les joueurs en fonction de leurs points.
        sorted_players = sorted(players_list, key=lambda p: p.score, reverse=True)

        # Étape 2 : Création des matchs en tenant compte des adversaires précédents.
        matched_players = []
        matches = []

        for i in range(0, len(sorted_players), 2):
            player1 = sorted_players[i]
            if player1 in matched_players:
                continue

            for j in range(i+1, len(sorted_players)):
                player2 = sorted_players[j]
                if player2 not in player1.previous_opponents and player2 not in matched_players:
                    matches.append((player1, player2))
                    player1.previous_opponents.append(player2)
                    player2.previous_opponents.append(player1)
                    matched_players.extend([player1, player2])
                    break

        return matches


    def save_tournament(self, tournament_name, players_list, current_round, current_match):
        # Convertir les joueurs en dictionnaires pour la sauvegarde
        players_data = [player.to_dict() for player in players_list]

        # Mettre à jour les joueurs dans le champ 'players' du tournoi et sauvegarder l'état actuel du round et du match
        self.db_tournament.update({
            "name": tournament_name,
            "list_player_save": players_data,
            "current_round": current_round,
            "current_match": current_match
        }, self.TournamentQuery.name == tournament_name)

