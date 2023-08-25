from Controller.Controllers import PlayerController
from Controller.Controllers import Menu

menu = Menu()
controller = PlayerController()

menu.set_gestion_joueurs(controller)
menu.set_gestion_tournoi(controller)

menu.display_principal_menu()
