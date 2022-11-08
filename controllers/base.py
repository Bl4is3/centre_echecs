"""Define the main controller."""

from models.player import Player
from models.tournament import Tournament
from tinydb import TinyDB
from pathlib import Path

tournaments = []
players = []


class Controller:
    """Main controller."""

    def __init__(self, view, id_tournament=1, id_player=1):
        """Has a deck, a list of players and a view."""
        # models
        self.view = view
        self.id_player = id_player
        self.id_tournament = id_tournament
        # a corriger car doit reprendre le dernier id de la table
        # si existante et non partir de 1 a chaque démarrage

    def create_player(self, detail):
        first_name = detail[0]
        last_name = detail[1]
        sex = detail[2]
        date_birthday = detail[3]
        rank = detail[4]
        id_player = self.id_player
        player = Player(id_player, first_name, last_name, sex,
                        date_birthday, rank)
        players.append(player)
        serialized_player = {
            'id': player.id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'sex': player.sex,
            'date_birthday': player.date_birthday,
            'rank': player.rank
        }
        self.id_player += 1

    def init_db(self):
        filename = r'db.json'
        fileobj = Path(filename)
        if fileobj.is_file():
            return
        else:
            db = TinyDB('db.json')
            players_table = db.table('players')
            tournaments_table = db.table('tournaments')
            players_table.truncate()
            tournaments_table.truncate()
        return db

    def get_datas_from_db(self):
        ...
        # db = self.init_db()
        # players_table = db.table('players')
        # tournaments_table = db.table('tournaments')
        # serialized_players = players_table.all()
        # serialized_tournaments = tournaments_table.all()

    def start_tournament(self, detail):
        name = detail[0]
        place = detail[1]
        date_beginning = detail[2]
        players = detail[3]
        timer = detail[4]
        description = detail[5]
        tournament = Tournament(self.id_tournament, name, place,
                                date_beginning, players, timer, description,
                                finished=False)
        tournaments.append(tournament)
        self.id_tournament += 1

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
        ranks = []
        for play in players:
            ranks.append(play.rank)
        sorted_ranks = sorted(ranks)
        sorted_player_by_ranks = []
        for rank in sorted_ranks:
            for player in players:
                if rank == player.rank:
                    sorted_player_by_ranks.append(player)
        return sorted_player_by_ranks

    def run(self):
        """Run the game."""
        running = True
        db = self.init_db()
        self.get_datas_from_db()
        choix = self.view.prompt_principal_menu()
        while running:
            if choix == "1":
                choix = self.view.afficher_menu_tournoi()
            elif choix == "11":
                if len(players) < 8:
                    print("Attention, Il n'y a pas suffisamment de joueurs"
                          "inscrits pour débuter un tournoi")
                    choix = self.view.afficher_menu_joueur()
                else:
                    choix = self.view.create_tournament()
            elif choix == "12":
                choix = self.view.resume_tournament()
            elif choix == "13":
                listing = self.view.show_listing_all_tournaments()
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
                test = self.sort_players_by_rank()
                self.view.affichage_liste_joueurs_classement(test)
                choix = self.view.afficher_menu_joueur()
            elif choix == "24":
                choix = self.view.prompt_principal_menu()
            elif choix == "3":
                return False
            else:
                print("Ce choix n'existe pas, merci de ré-essayer")
                choix = self.view.prompt_principal_menu()
