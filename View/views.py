class Views_menu:

    @staticmethod
    def view_principal_menu(self):
        print("\nMenu principal:")
        print("1. Gérer les joueurs")
        print("2. Gérer les tournois")
        print("3. Quitter")

        principal_menu_choice = input("Veuillez faire un choix : ")
        return principal_menu_choice

    @staticmethod
    def view_player_menu(self):
        print("\nMenu gestion des joueurs:")
        print("1. Ajouter un joueur")
        print("2. Supprimer un joueur")
        print("3. Modifier un joueur")
        print("4. Retour au menu principal")

        player_menu_choice = input("Veuillez faire un choix : ")
        return player_menu_choice

    @staticmethod
    def view_tournament_menu(self):
        print("\nMenu gestion des tournoi:")
        print("1. Créer un tournoi")
        print("2. Modifier un tournoi")
        print("3. Supprimer un tournoi")
        print("4. Reprendre la création d'un tournoi")

        tournament_menu_choice = input("Veuillez faire un choix : ")
        return tournament_menu_choice

class Messages:

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






