class Views:

    @staticmethod
    def view_principal_menu():
        print("\nMenu principal:")
        print("1. Gérer les joueurs")
        print("2. Gérer les tournois")
        print("3. Quitter")

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
        print("4. Reprendre la création d'un tournoi")

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
        print("Tournoi non trouvé")

    @staticmethod
    def message_modifie_tournament():
        print("Tournoi modifié")

