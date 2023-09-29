from Controller.Controllers import PlayerController, TournamentController
from Controller.Controllers import Menu
from Controller.Controllers import ReportController

menu = Menu()
player_controller = PlayerController()
tournament_controller = TournamentController()
report_controller = ReportController()

menu.set_player_admin(player_controller)
menu.set_tournament_admin(tournament_controller)
menu.set_report_admin(report_controller)

menu.display_principal_menu()
