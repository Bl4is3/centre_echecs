"""Define the main controller."""

from models.player import Player
from views.view import View

tournaments = []
players = []


class Controller:
    """Main controller."""

    def __init__(self, view):
        """Has a deck, a list of players and a view."""
        # models
        self.view = view

    def create_player(self, detail):
        first_name = detail[0]
        last_name = detail[1]
        sex = detail[2]
        date_birthday = detail[3]
        rank = detail[4]
        player = Player(first_name, last_name, sex, date_birthday, rank)
        players.append(player)

    def start_game(self):
        ...

    def sort_players_by_names(self):
        names = []
        for play in players:
            names.append(play.first_name)
        sorted_names = sorted(names)
        sorted_player_by_names = []
        for name in sorted_names:
            for player in players:
                if name == player.first_name:
                    sorted_player_by_names.append(player)
        return sorted_player_by_names

    def sort_players_by_rank(self):
        self.players = players
        ranks = []
        for player in players:
            rank = player["rank"]
            ranks.append(rank)
        sorted_ranks = sorted(ranks)
        sorted_player_by_ranks = []
        for rank in sorted_ranks:
            for player in players:
                if rank == player["rank"]:
                    sorted_player_by_ranks.append(player)
        return sorted_player_by_ranks

    def run(self):
        """Run the game."""

        running = True
        choix = self.view.prompt_principal_menu()
        while running:

            if choix == "1":
                choix = self.view.afficher_menu_tournoi()
            elif choix == "11":
                choix = self.view.begin_tournament()
            elif choix == "12":
                choix = self.view.resume_tournament()
            elif choix == "13":
                listing = self.view.show_listing_tournaments()
                choix = self.view.affichage_liste_joueurs_classement(listing)
            elif choix == "16":
                choix = self.view.prompt_principal_menu()
            elif choix == "15":
                return False
            elif choix == "2":
                choix = self.view.afficher_menu_joueur()
            elif choix == "21":
                detail = self.view.add_player()
                self.create_player(detail)
                choix = self.view.afficher_menu_joueur()
            elif choix == "22":
                listing = self.sort_players_by_names()
                self.view.affichage_liste_joueurs_alphabetique(listing)
                choix = self.view.afficher_menu_joueur()
            elif choix == "23":
                listing = self.sort_players_by_rank()
                self.view.affichage_liste_joueurs_classement(listing)
                choix = self.view.afficher_menu_joueur()
            elif choix == "24":
                choix = self.view.prompt_principal_menu()
            elif choix == "3":
                return False
            else:
                print("Ce choix n'existe pas, merci de recommencer")
                choix = self.view.prompt_principal_menu()


