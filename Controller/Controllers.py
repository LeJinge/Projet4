import json

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
        self.TournamentQuery = Query()
        self.PlayerQuery = Query()

    def get_user_choice_tournament(self):

        Views.view_tournament_menu()
        tournament_menu_choice = input("Veuillez faire un choix : ")

        if tournament_menu_choice == "1":
            self.create_tournament()
        if tournament_menu_choice == "2":
            self.modify_tournament()
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

    def create_tournament(self):
        new_tournament = Tournament()
        self.get_tournament_details(new_tournament)
        self.add_players_to_tournament(new_tournament)
        serialized_players = self.serialize_players(new_tournament.list_player_save)
        self.save_tournament_to_db(new_tournament, serialized_players)

    def get_tournament_details(self, tournament, prompt="Entrez les informations pour le tournoi:"):
        print(prompt)
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
        existing_player = self.db_players.get(self.PlayerQuery.chess_id == player.chess_id)
        if not existing_player or player.chess_id != existing_player['chess_id']:
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

        self.get_tournament_details(tournament_found, "Entrez les nouvelles informations pour le tournoi:")
        self.add_players_to_tournament(tournament_found)
        serialized_players = self.serialize_players(tournament_found.list_player_save)
        self.update_tournament_in_db(tournament_found, serialized_players)
        Views.message_modifie_tournament()

    def get_tournament_by_name(self, name):
        data = self.db_tournament.get(self.TournamentQuery.name == name)
        if data:
            return Tournament.from_dict(data)
        return None

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
        self.db_tournament.remove(self.TournamentQuery.name == tournament.name)

    def get_tournament_by_name(self, name):
        return self.db_tournament.search(self.TournamentQuery.name == name)[0]

    def start_tournament(self):
        # Étape 1: Récupération du nom du tournoi
        tournament_name = input("Entrez le nom du tournoi que vous voulez commencer: ")

        # Étape 2: Récupération des données du tournoi
        tournament_data = self.get_tournament_by_name(tournament_name)
        players_list = [Player.from_dict(data) for data in tournament_data['list_player_save']]

        # Étape 3: Création du premier round si la liste des tours est vide
        if not tournament_data['list_tours']:
            initial_round = self.generate_initial_rounds(players_list, 1)  # Un seul tour à générer
            tournament_data['list_tours'] = initial_round
            self.save_tournament(tournament_name, tournament_data['list_tours'], 0)  # Enregistrement initial

        rounds = tournament_data['list_tours']
        current_round_index = tournament_data.get('current_round', 0)

        while current_round_index < len(rounds):  # Pour chaque tour jusqu'à la fin
            round_data = rounds[current_round_index]
            print(f"\nDébut du {round_data['name']}!")

            # Étape 4 & 5 : Déroulement de chaque match du tour actuel
            for match_data in round_data['matches']:
                print(f"{match_data['player1']} vs {match_data['player2']}")

                while True:
                    winner_id = input(
                        f"Qui est le vainqueur ? 1. {match_data['player1']} 2. {match_data['player2']} : ")

                    if winner_id == "1":
                        match_data['winner'] = match_data['player1']
                        self.update_player_score_in_json(tournament_name, match_data['player1'], 1)
                        break
                    elif winner_id == "2":
                        match_data['winner'] = match_data['player2']
                        self.update_player_score_in_json(tournament_name, match_data['player2'], 1)
                        break
                    else:
                        print("Choix non valide. Veuillez sélectionner le bon numéro.")

                # Sauvegarde après chaque match
                self.save_tournament(tournament_name, rounds, current_round_index)

                # Possibilité de quitter après chaque match
                exit_choice = input("Voulez-vous quitter le tournoi? (Oui/Non): ").lower()
                if exit_choice == 'oui':
                    return

            print(f"Fin du {round_data['name']}!\n")

            if current_round_index + 1 == tournament_data['rounds_numbers']:
                print("Le tournoi est terminé!")
                return  # sortir de la méthod
            # Mise à jour des scores
            for match in round_data['matches']:
                for player in players_list:
                    if match['winner'] == player.first_name:
                        player.score += 1

            # Étape 6 & 7: Générer le tour suivant et continuer
            next_round_matches = self.generate_matches(players_list)

            matches_data = [{'player1': match[0].first_name, 'player2': match[1].first_name, 'winner': None} for match
                            in next_round_matches]

            next_round_data = {
                'name': f"Tour {current_round_index + 2}",
                'matches': matches_data
            }

            rounds.append(next_round_data)
            self.save_tournament(tournament_name, rounds, current_round_index + 1)
            current_round_index += 1

    def generate_initial_rounds(self, players_list, rounds_numbers):

        rounds_data = []

        # Faire une copie superficielle de la liste des joueurs pour éviter de modifier la liste originale
        remaining_players = players_list.copy()

        # Pour chaque ronde
        for i in range(rounds_numbers):
            round_name = f"Tour {i + 1}"
            matches = []

            # Pour chaque match de la ronde
            for _ in range(len(remaining_players) // 2):
                match_data = {
                    'player1': remaining_players.pop().first_name,
                    'player2': remaining_players.pop().first_name,
                    'winner': None
                }
                matches.append(match_data)

            rounds_data.append({
                'name': round_name,
                'matches': matches
            })

        return rounds_data

    def generate_matches(self, players_list_save):
        # Étape 1 : Trier les joueurs en fonction de leurs points.
        sorted_players = sorted(players_list_save, key=lambda p: p.score, reverse=True)

        # Étape 2 : Création des matchs en tenant compte des adversaires précédents.
        matched_players = set()
        matches = []

        for player1 in sorted_players:
            if player1 in matched_players:
                continue

            for player2 in sorted_players:
                if player2 == player1 or player2 in matched_players:
                    continue
                if player2 not in player1.previous_opponents:
                    matches.append((player1, player2))
                    player1.previous_opponents.append(player2)
                    player2.previous_opponents.append(player1)
                    matched_players.add(player1)
                    matched_players.add(player2)
                    break

        return matches

    def save_tournament(self, tournament_name, rounds_data, current_round_index):
        self.db_tournament.update({
            "list_tours": rounds_data,
            "current_round": current_round_index + 1
        }, self.TournamentQuery.name == tournament_name)

    def update_player_score_in_json(self, tournament_name, player_name, score_increment):
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

    def resume_tournament(self):
        tournament_name = input("Entrez le nom du tournoi que vous voulez reprendre: ")

        # Étape 1 : Récupération des données du tournoi
        tournament_data = self.get_tournament_by_name(tournament_name)
        if not tournament_data:
            print(f"Le tournoi {tournament_name} n'existe pas.")
            return

        rounds = tournament_data['list_tours']
        current_round_index = tournament_data.get('current_round', 0)

        # Étape 2 : Identifier le tour et le match non terminés
        round_to_resume = None
        match_to_resume_index = None

        for r, round_data in enumerate(rounds[current_round_index:], start=current_round_index):
            for m, match_data in enumerate(round_data['matches']):
                if not match_data['winner']:
                    round_to_resume = round_data
                    match_to_resume_index = m
                    break
            if round_to_resume:
                break

        # Si aucun match non joué n'est trouvé
        if not round_to_resume:
            print(f"Le tournoi {tournament_name} a déjà été terminé.")
            return

        # Étape 3 : Reprendre le tournoi à partir du match non joué
        print(f"\nReprise du {round_to_resume['name']} à partir du match {match_to_resume_index + 1}!")

        for match_data in round_to_resume['matches'][match_to_resume_index:]:
            print(f"{match_data['player1']} vs {match_data['player2']}")

            while True:
                winner_id = input(
                    f"Qui est le vainqueur ? 1. {match_data['player1']} 2. {match_data['player2']} : ")

                if winner_id == "1":
                    match_data['winner'] = match_data['player1']
                    self.update_player_score_in_json(tournament_name, match_data['player1'], 1)
                    break
                elif winner_id == "2":
                    match_data['winner'] = match_data['player2']
                    self.update_player_score_in_json(tournament_name, match_data['player2'], 1)
                    break
                else:
                    print("Choix non valide. Veuillez sélectionner le bon numéro.")

            # Sauvegarde après chaque match
            self.save_tournament(tournament_name, rounds, r)

            # Vérifiez si l'utilisateur veut arrêter après le match
            exit_choice = input("Voulez-vous quitter le tournoi? (Oui/Non): ").lower()
            if exit_choice == 'oui':
                return









