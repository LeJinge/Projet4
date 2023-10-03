from tinydb import TinyDB, Query
from Model.player import Player
from Model.match import Match
from Model.round import Round
from Model.tournament import Tournament
from View.views import Views
from tinydb.storages import JSONStorage
import random


class Menu:

    def __init__(self):
        self.player_admin = None
        self.tournament_admin = None
        self.report_admin = None

    def set_player_admin(self, gestion_joueurs):
        self.player_admin = gestion_joueurs

    def set_tournament_admin(self, tournament_admin):
        self.tournament_admin = tournament_admin

    def set_report_admin(self, report_admin):
        self.report_admin = report_admin

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
                    Views.message_error_player()
            elif principal_menu_choice == "2":
                if self.tournament_admin:
                    self.tournament_admin.get_user_choice_tournament()
                else:
                    Views.message_error_tournament()
            elif principal_menu_choice == "3":
                if self.report_admin:
                    self.report_admin.get_user_choice_report()
                else:
                    Views.message_error_tournament()
            elif principal_menu_choice == "4":
                Views.message_goodbye()
                break
            else:
                Views.message_non_valid_choice()


class PlayerController:

    def __init__(self):
        self.db_players = TinyDB(
            'players.json', storage=JSONStorage, encoding='utf-8')
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
                Views.insert_error(e)

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
        identifiant_a_effacer = input(
            "Entrez l'Identifiant National d'échec du joueur à effacer : ")

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
        chess_id = input(
            "Entrez l'Identifiant National "
            "d'échec du joueur que vous souhaitez modifier : ")
        last_name = input(
            "Entrez le nom du joueur que vous souhaitez modifier : ")
        first_name = input(
            "Entrez le prénom du joueur que vous souhaitez modifier : ")

        player_found = self.db_players.get(
            (self.PlayerQuery.chess_id == chess_id) &
            (self.PlayerQuery.last_name == last_name) &
            (self.PlayerQuery.first_name == first_name)
        )

        if not player_found:
            Views.message_player_not_found()
            return

        Views.message_new_information_player()
        new_last_name = input("Nom : ")
        new_first_name = input("Prénom : ")
        new_birth_date = input("Date de naissance (format YYYY-MM-DD) : ")
        new_chess_id = input("Nouvel Identifiant National d'échec : ")

        self.db_players.update({
            "last_name": new_last_name,
            "first_name": new_first_name,
            "birth_date": new_birth_date,
            "chess_id": new_chess_id
        }, (self.PlayerQuery.last_name == last_name) &
           (self.PlayerQuery.first_name == first_name) &
           (self.PlayerQuery.chess_id == chess_id))

        Views.message_modifie_player()

    def recover_player(self, last_name=None, first_name=None, chess_id=None):

        # Recherche par identifiant
        if chess_id:
            joueur_dict = \
                self.db_players.get(self.PlayerQuery.chess_id == chess_id)

        # Recherche par nom et prénom
        elif last_name & first_name:
            joueur_dict = self.db_players.get(
                (self.PlayerQuery.last_name == last_name) &
                (self.PlayerQuery.first_name == first_name))

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
        self.db_tournament = TinyDB('tournament.json',
                                    storage=JSONStorage, encoding='utf-8')
        self.db_players = TinyDB('players.json',
                                 storage=JSONStorage, encoding='utf-8')
        self.TournamentQuery = Query()
        self.PlayerQuery = Query()

    def get_user_choice_tournament(self):

        Views.view_tournament_menu()
        tournament_menu_choice = input("Veuillez faire un choix : ")

        if tournament_menu_choice == "1":
            self.create_tournament()
        elif tournament_menu_choice == "2":
            self.modify_tournament()
        elif tournament_menu_choice == "3":
            self.delete_tournament()
        elif tournament_menu_choice == "4":
            self.start_or_resume_tournament()
        elif tournament_menu_choice == "5":
            return
        else:
            Views.message_non_valid_choice()

    def create_tournament(self):
        new_tournament = Tournament()
        self.get_tournament_details(new_tournament)
        self.add_players_to_tournament(new_tournament)
        serialized_players = \
            self.serialize_players(new_tournament.list_player_save)
        self.save_tournament_to_db(new_tournament, serialized_players)

    def get_tournament_details(self, tournament):
        Views.message_tournament_information()
        tournament.name = input("Nom : ")
        tournament.place = input("Lieu : ")
        tournament.start_date = input("Date de début : ")
        tournament.end_date = input("Date de fin : ")
        tournament.rounds_numbers = int(input("Nombre de tours : "))

    def add_players_to_tournament(self, tournament):
        for _ in range(tournament.rounds_numbers * 2):
            new_player = PlayerController.create_player(self)
            tournament.list_player_save.append(new_player)
            self.save_player_to_db(new_player)

    def save_player_to_db(self, player):
        existing_player = self.db_players.get(
            self.PlayerQuery.chess_id == player.chess_id)
        if not existing_player or \
                player.chess_id != existing_player['chess_id']:
            self.db_players.insert(player.to_dict())

    def serialize_players(self, players):
        return [player.to_dict() for player in players]

    def save_tournament_to_db(self, tournament, serialized_players):
        self.db_tournament.insert(
            {
                "name": tournament.name,
                "place": tournament.place,
                "start_date": tournament.start_date,
                "end_date": tournament.end_date,
                "rounds_numbers": tournament.rounds_numbers,
                "list_player_save": serialized_players,
                "list_tours": tournament.list_tours,
                "current_round": tournament.current_round
            }
        )

    def modify_tournament(self):
        name_modifie_tournament = input("Entrez le nom du tournoi : ")
        tournament_found = self.get_tournament_by_name(name_modifie_tournament)

        if not tournament_found:
            Views.message_tournament_not_found()
            return

        self.get_tournament_details(
            tournament_found,
            "Entrez les nouvelles informations pour le tournoi:")
        self.add_players_to_tournament(tournament_found)
        serialized_players = self.serialize_players(
            tournament_found.list_player_save)
        self.update_tournament_in_db(tournament_found, serialized_players)
        Views.message_modifie_tournament()

    def update_tournament_in_db(self, tournament, serialized_players):
        self.db_tournament.update({
            "name": tournament.name,
            "place": tournament.place,
            "start_date": tournament.start_date,
            "end_date": tournament.end_date,
            "rounds_numbers": tournament.rounds_numbers,
            "list_player_save": serialized_players,
            "list_tours": tournament.list_tours
        })

    def delete_tournament(self):
        name_to_delete = input("Entrez le nom du tournoi à supprimer : ")
        tournament_to_delete = self.get_tournament_by_name(name_to_delete)

        if not tournament_to_delete:
            Views.message_tournament_not_found()
            return

        self.remove_tournament_from_db(tournament_to_delete)
        Views.message_tournament_deleted()

    def remove_tournament_from_db(self, tournament):
        self.db_tournament.remove(
            self.TournamentQuery.name == tournament['name'])

    def get_tournament_by_name(self, name):
        return self.db_tournament.search(
            self.TournamentQuery.name == name)[0]

    def generate_initial_matches(self, tournament):
        players = tournament.list_player_save.copy()
        random.shuffle(players)
        matches = []

        while players:
            player1 = players.pop()
            player2 = players.pop()

            match = Match(player1, player2)
            matches.append(match)

            player1.previous_opponents.append(player2.chess_id)
            player2.previous_opponents.append(player1.chess_id)

        round_obj = Round()
        round_obj.matchs = matches
        round_obj.name = "Tour 1"
        tournament.list_tours.append(round_obj)

        self.save_tournament(tournament)

        return matches

    def generate_next_matches(self, tournament):
        # Triez les joueurs par score
        players = sorted(
            tournament.list_player_save, key=lambda p: p.score, reverse=True)
        matches = []

        # Associez les joueurs par paires
        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1] if i + 1 < len(players) else None

            if not player2:
                matches.append(Match(player1, None))
                continue

            if player2.chess_id in player1.previous_opponents:
                for j in range(i + 2, len(players)):
                    if players[j].chess_id not in player1.previous_opponents:
                        # Échangez les joueurs
                        player2, players[j] = players[j], player2
                        break

            match = Match(player1, player2)
            matches.append(match)

            player1.previous_opponents.append(player2.chess_id)
            player2.previous_opponents.append(player1.chess_id)

        round_obj = Round()
        round_obj.matchs = matches
        round_obj.name = f"Tour {len(tournament.list_tours) + 1}"
        tournament.list_tours.append(round_obj)

        self.save_tournament(tournament)

        return matches

    def save_tournament(self, tournament):
        tournament_name = tournament.name

        # Sérialisez chaque round en un dictionnaire avant de le stocker
        rounds_data = [round_obj.to_dict() for
                       round_obj in tournament.list_tours]

        # Assurez-vous que les objets Player sont sérialisés
        for round_data in rounds_data:
            for match in round_data["matchs"]:
                if not isinstance(match["player1"], dict):
                    match["player1"] = match["player1"].to_dict()
                if not isinstance(match["player2"], dict):
                    match["player2"] = match["player2"].to_dict()

        updated_players_data = [player.to_dict() for
                                player in tournament.list_player_save]

        self.db_tournament.update({
            "list_player_save": updated_players_data,
            "list_tours": rounds_data,
            "current_round": len(tournament.list_tours)
        }, self.TournamentQuery.name == tournament_name)

    def update_and_save(self, tournament, match_obj, winner_id):
        if winner_id == "1":
            match_obj.player1.score += 1
            self.update_player_score_in_json(
                tournament.name, match_obj.player1.first_name, 1)
        elif winner_id == "2":
            match_obj.player2.score += 1
            self.update_player_score_in_json(
                tournament.name, match_obj.player2.first_name, 1)
        elif winner_id == "3":  # Match nul
            match_obj.player1.score += 0.5
            match_obj.player2.score += 0.5
            self.update_player_score_in_json(
                tournament.name, match_obj.player1.first_name, 0.5)
            self.update_player_score_in_json(
                tournament.name, match_obj.player2.first_name, 0.5)

        match_obj.completed = True  # Marquez le match comme complet
        self.save_tournament(tournament)

    def update_player_score_in_json(
            self, tournament_name, player_name, score_increment):
        # Récupération des données actuelles
        tournament_data = self.get_tournament_by_name(tournament_name)
        players_data = tournament_data['list_player_save']

        # Mise à jour du score
        for player_data in players_data:
            if player_data['first_name'] == player_name:
                player_data['score'] += score_increment
                break

        # Sauvegarde des données mises à jour
        self.db_tournament.update({
            "list_player_save": players_data
        }, self.TournamentQuery.name == tournament_name)

    def start_or_resume_tournament(self):
        # Étape 1: Récupération du nom du tournoi
        tournament_name = input(
            "Entrez le nom du tournoi que vous voulez commencer ou reprendre: "
        )

        # Étape 2: Récupération des données du tournoi
        tournament_data = self.get_tournament_by_name(tournament_name)
        if not tournament_data:
            Views.tournament_not_exist(tournament_name)
            return

        tournament = Tournament.from_dict(tournament_data)

        # Si le tournoi n'a pas encore commencé, initialisez-le
        if not tournament.list_tours:
            self.generate_initial_matches(tournament)

        while tournament.current_round <= tournament.rounds_numbers:
            current_round = tournament.list_tours[tournament.current_round - 1]
            Views.debut_turn(current_round.name)

            if not current_round.matchs:
                self.generate_next_matches(tournament)

            for match_obj in current_round.matchs:
                if match_obj.completed:
                    continue  # si le match est déjà terminé, passez au suivant

                Views.display_match(match_obj.player1.first_name, match_obj.player2.first_name)

                while True:
                    winner_id = input(
                        f"Qui est le vainqueur ? "
                        f"1. {match_obj.player1.first_name} "
                        f"2. {match_obj.player2.first_name} "
                        f"3. Match nul : ")
                    if winner_id in ["1", "2", "3"]:
                        self.update_and_save(tournament, match_obj, winner_id)
                        break
                    else:
                        Views.message_non_valid_choice()

                exit_choice = input(
                    "Voulez-vous quitter le tournoi? (Oui/Non): ").lower()
                if exit_choice in ['oui', 'o', 'y']:
                    return

            # Vérification de la fin du tour en cours
            if all(match.completed for match in current_round.matchs):
                Views.end_turn(current_round.name)
                tournament.current_round += 1

                if tournament.current_round <= tournament.rounds_numbers:
                    self.generate_next_matches(tournament)

        Views.end_tournament()

        # Affichage du classement des participants à la fin du tournoi
        sorted_players = self.get_sorted_players_by_score(tournament_name)
        Views.display_ranking(sorted_players)

    def get_sorted_players_by_score(self, tournament_name):
        tournament_data = self.get_tournament_by_name(tournament_name)
        players_data = tournament_data['list_player_save']

        # Trier les joueurs en fonction de leur score
        sorted_players = sorted(
            players_data, key=lambda x: x['score'], reverse=True)

        return sorted_players


class ReportController:
    def __init__(self):
        self.db_players = TinyDB('players.json')
        self.db_tournament = TinyDB('tournament.json')

    def get_user_choice_report(self):

        Views.view_report_menu()
        report_menu_choice = input("Veuillez faire un choix : ")

        if report_menu_choice == "1":
            self.list_players_alphabetical()
        elif report_menu_choice == "2":
            self.list_all_tournaments()
        elif report_menu_choice == "3":
            self.tournament_details()
        elif report_menu_choice == "4":
            self.list_tournament_players()
        elif report_menu_choice == "5":
            self.list_rounds_matches()
        elif report_menu_choice == "6":
            self.final_ranking()
        elif report_menu_choice == "7":
            return
        else:
            Views.message_non_valid_choice()

    def get_tournament_by_name(self, name):
        return self.db_tournament.search(self.TournamentQuery.name == name)[0]

    def list_players_alphabetical(self):
        players = self.db_players.table('_default').all()
        sorted_players = sorted(players, key=lambda x: x['last_name'])

        Views.display_players_alphabetical(sorted_players)

    def list_all_tournaments(self):
        tournaments = self.db_tournament.table('_default').all()
        for tournament in tournaments:
            Views.display_all_tournament(tournaments)

    def tournament_details(self):
        tournament_name = input("Veuillez entrer le nom du tournoi : ")

        tournament_data = Query()
        tournament = \
            self.db_tournament.table(
                '_default'
            ).get(
                tournament_data.name == tournament_name
            )
        if tournament:
            Views.display_tournament_details(tournament)
        else:
            Views.message_tournament_not_found()

    def list_tournament_players(self):
        tournament_name = input(
            "Veuillez entrer le nom du tournoi : ")

        tournament_data = Query()
        tournament = \
            self.db_tournament.table(
                '_default'
            ).get(
                tournament_data.name == tournament_name
            )
        if tournament:
            players = sorted(
                tournament['list_player_save'], key=lambda x: x['last_name'])

            Views.display_tournament_players(players)
        else:
            Views.message_tournament_not_found()

    def list_rounds_matches(self):
        tournament_name = input(
            "Veuillez entrer le nom du tournoi : ")

        tournament_data = Query()
        tournament = self.db_tournament.table(
            '_default'
        ).get(
            tournament_data.name == tournament_name
        )
        if tournament:
            Views.display_turn_and_round(tournament)
        else:
            Views.message_tournament_not_found()

    def final_ranking(self):
        tournament_name = input("Veuillez entrer le nom du tournoi : ")

        tournament_data = Query()
        tournament = self.db_tournament.table(
            '_default'
        ).get(
            tournament_data.name == tournament_name
        )
        players_data = tournament['list_player_save']

        # Trier les joueurs en fonction de leur score
        sorted_players = sorted(
            players_data, key=lambda x: x['score'], reverse=True
        )
        Views.display_final_ranking(sorted_players)
