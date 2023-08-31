from Controller.Controllers import PlayerController, TournamentController
from Controller.Controllers import Menu

menu = Menu()
player_controller = PlayerController()
tournament_controller = TournamentController()

menu.set_player_admin(player_controller)
menu.set_tournament_admin(tournament_controller)

menu.display_principal_menu()
