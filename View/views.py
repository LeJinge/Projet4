class Views:

    @staticmethod
    def view_principal_menu():
        print("\nMenu principal:")
        print("1. Gérer les joueurs")
        print("2. Gérer les tournois")
        print("3. Rapports")
        print("4. Quitter")

    @staticmethod
    def view_player_menu():
        print("\nMenu gestion des joueurs:")
        print("1. Ajouter un joueur")
        print("2. Supprimer un joueur")
        print("3. Modifier un joueur")
        print("4. Retour au menu principal")

    @staticmethod
    def view_tournament_menu():
        print("\nMenu gestion des tournoi:")
        print("1. Créer un tournoi")
        print("2. Modifier un tournoi")
        print("3. Supprimer un tournoi")
        print("4. Commencer un tournoi")
        print("5. Retour")

    @staticmethod
    def view_report_menu():
        print("\nMenu gestion des tournoi:")
        print("1. Liste des joueurs")
        print("2. Liste des tournois")
        print("3. Date d'un tournoi")
        print("4. Participants d'un tournoi")
        print("5. Rapport match et tour d'un tournoi")
        print("6. Classement par tournoi")
        print("7. Retour")

    @staticmethod
    def message_player_exist():
        print("Ce joueur existe déjà.")

    @staticmethod
    def message_player_duplicate():
        print("Ce joueur existe déjà dans la liste, doublon non ajouté.")

    @staticmethod
    def message_new_player_added():
        print("Nouveau joueur ajouté avec succès!")

    @staticmethod
    def message_non_valid_choice():
        print("Choix non reconnu. Veuillez choisir une option valide.")

    @staticmethod
    def message_modifie_player():
        print("Le joueur a été modifié avec succès!")

    @staticmethod
    def message_new_tournament_added():
        print("Nouveau tournoi créé avec succès!")

    @staticmethod
    def message_delete_player():
        print("Le joueur a bien été supprimé!")

    @staticmethod
    def message_player_not_found():
        print("Joueur non trouvé.")

    @staticmethod
    def message_tournament_not_found():
        print("Tournoi non trouvé.")

    @staticmethod
    def message_modifie_tournament():
        print("Tournoi modifié")

    @staticmethod
    def message_tournament_deleted():
        print("Tournoi supprimé")

    @staticmethod
    def message_error_player():
        print("Erreur: La gestion des joueurs n'est pas configurée.")

    @staticmethod
    def message_error_tournament():
        print("Erreur: La gestion des tournois n'est pas configurée.")

    @staticmethod
    def message_goodbye():
        print("Au revoir!")

    @staticmethod
    def message_new_information_player():
        print("Entrez les nouvelles informations pour le joueur:")

    @staticmethod
    def message_tournament_information():
        print("Entrez les informations pour le tournoi:")

    @staticmethod
    def insert_error(message):
        print(f"Erreur lors de l'insertion: {message}")

    @staticmethod
    def tournament_not_exist(nom):
        print(f"Le tournoi {nom} n'existe pas.")

    @staticmethod
    def debut_turn(nom_du_tour):
        print(f"\nDébut de {nom_du_tour}!")

    @staticmethod
    def display_match(player1_name, player2_name):
        print(f"{player1_name} vs {player2_name}")

    @staticmethod
    def end_turn(nom_du_tour):
        print(f"Fin de {nom_du_tour}!\n")

    @staticmethod
    def end_tournament():
        print("Le tournoi est terminé!")

    @staticmethod
    def display_ranking(players):
        print("\nClassement des participants:")
        for index, player in enumerate(players, 1):
            print(f"{index}. {player['first_name']} "
                  f"{player['last_name']} - Score: {player['score']}")

    @staticmethod
    def display_players_alphabetical(players):
        for player in players:
            print(f"{player['first_name']} {player['last_name']}")

    @staticmethod
    def display_all_tournament(tournaments):
        for tournament in tournaments:
            print(tournament['name'])

    @staticmethod
    def display_tournament_details(tournament):
        print(f"Name: {tournament['name']}")
        print(f"Start Date: {tournament['start_date']}")
        print(f"End Date: {tournament['end_date']}")

    @staticmethod
    def display_tournament_players(players):
        for player in players:
            print(f"{player['first_name']} {player['last_name']}")

    @staticmethod
    def display_turn_and_round(tournament):
        for round_ in tournament['list_tours']:
            print(f"Round Name: {round_['name']}")
            for match in round_['matchs']:
                print(
                    f"Match: {match['player1']['first_name']} "
                    f"{match['player1']['last_name']} vs "
                    f"{match['player2']['first_name']} "
                    f"{match['player2']['last_name']}")

    @staticmethod
    def display_final_ranking(players):
        print("\nClassement des participants:")
        for index, player in enumerate(players, 1):
            print(f"{index}. "
                  f"{player['first_name']} "
                  f"{player['last_name']} - Score: {player['score']}")