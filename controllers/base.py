"""Define the main controller."""

from models.player import Player
from models.tournament import Tournament
from tinydb import TinyDB, Query
from pathlib import Path


class Controller:
    """Main controller."""

    def __init__(self, view):
        """Has a a view."""
        # models
        self.view = view

    def create_player(self, detail):
        """ Instance a new player"""
        first_name = detail[0]
        last_name = detail[1]
        sex = detail[2]
        date_birthday = detail[3]
        rank = detail[4]
        id_player = self.get_last_id('players') + 1
        player = Player(id_player, first_name, last_name, sex,
                        date_birthday, rank)
        serialized_player = self.serialized_player(player)
        self.add_player_to_db(serialized_player)

    @staticmethod
    def serialized_player(player):
        """Serialize a player"""
        # player = Player(self.id_player, detail[0], detail[1], detail[2],
        #                 detail[3], detail[4])
        serialized_player = {
            'id': player.id,
            'first_name': player.first_name,
            'last_name': player.last_name,
            'sex': player.sex,
            'date_birthday': player.date_birthday,
            'rank': player.rank
        }
        return serialized_player

    @staticmethod
    def unserialized_player(serialized_player):
        """Unserialize a player"""
        id_player = serialized_player['id']
        first_name = serialized_player['first_name']
        last_name = serialized_player['last_name']
        sex = serialized_player['sex']
        date_birthday = serialized_player['date_birthday']
        rank = serialized_player['rank']

        return Player(
            id_player,
            first_name,
            last_name,
            sex,
            date_birthday,
            rank)

    def serialized_tournament(self, tournament):
        """Serialize a tournament"""
        serialized_tournament = {
            'id': tournament.id,
            'first_name': tournament.first_name,
            'last_name': tournament.last_name,
            'sex': tournament.sex,
            'date_birthday': tournament.date_birthday,
            'rank': tournament.rank
        }
        return serialized_tournament

    def unserialized_tournament(self, serialized_tournament):
        """Unserialize a tournament"""
        id_tournament = serialized_tournament['id']
        name = serialized_tournament['name']
        place = serialized_tournament['place']
        date_beginning = serialized_tournament['date_beginning']
        players_tournament = serialized_tournament['players_tournament']
        timer = serialized_tournament['timer']
        description = serialized_tournament['description']
        finished = serialized_tournament['finished']
        return Tournament(
            id_tournament,
            name,
            place,
            date_beginning,
            players_tournament,
            timer,
            description,
            finished)

    @staticmethod
    def initialize_database():
        """Create database  and tables (if not exist)"""
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

    def get_players_from_db(self):
        """ Get players from db"""
        db = TinyDB('db.json')
        players_table = db.table('players')
        serialized_players = players_table.all()
        return serialized_players

    @staticmethod
    def get_tournaments_from_db():
        """ Get tournaments from db"""
        db = TinyDB('db.json')
        tournaments_table = db.table('tournaments')
        serialized_tournaments = tournaments_table.all()
        return serialized_tournaments

    def add_player_to_db(self, serialized_player):

        db = TinyDB('db.json')
        players_table = db.table('players')
        players_table.insert(serialized_player)

    def add_tournament_to_db(self, serialized_tournament):
        db = TinyDB('db.json')
        tournaments_table = db.table('tournaments')
        tournaments_table.insert(serialized_tournament)

    def start_tournament(self, detail):
        name = detail[0]
        place = detail[1]
        date_beginning = detail[2]
        players_tournament = detail[3]
        timer = detail[4]
        description = detail[5]
        id_tournament = self.get_last_id('tournaments') + 1
        tournament = Tournament(
            id_tournament,
            name,
            place,
            date_beginning,
            players_tournament,
            timer,
            description,
            finished=False)
        serialized_tournament = self.serialized_tournament(tournament)
        self.add_tournament_to_db(serialized_tournament)


    @staticmethod
    def get_list_tournaments_not_finished():
        """ Get tournaments in progress"""
        db = TinyDB('db.json')
        all_tournaments = db.table('tournaments')
        list_tournaments = Query()
        tournaments_in_progress = all_tournaments.search(
            list_tournaments.finished == 'False')
        return tournaments_in_progress

    def get_last_id(self, element):
        db = TinyDB('db.json')
        name_table = str(element)
        elements = db.table(name_table)
        el = elements.all()[-1]
        last_id = el.doc_id
        return last_id

    def get_number_of_players(self):
        db = TinyDB('db.json')
        elements = db.table('players')
        number = len(elements)
        return number

    def sort_players_by_names(self, players):
        names = []
        for play in players:
            unserialized_player = self.unserialized_player(play)
            names.append(unserialized_player.last_name)
        sorted_names = sorted(names)
        sorted_player_by_names = []
        for name in sorted_names:
            for player in players:
                unserialized_player = self.unserialized_player(player)
                if name == unserialized_player.last_name:
                    sorted_player_by_names.append(unserialized_player)
        return sorted_player_by_names

    def sort_players_by_rank(self, players):
        ranks = []
        for play in players:
            unserialized_player = self.unserialized_player(play)
            ranks.append(unserialized_player.rank)
        sorted_ranks = sorted(ranks)
        sorted_player_by_ranks = []
        for rank in sorted_ranks:
            for player in players:
                unserialized_player = self.unserialized_player(player)
                if rank == unserialized_player.rank:
                    sorted_player_by_ranks.append(unserialized_player)
        return sorted_player_by_ranks

    def run(self):
        """Run the game."""
        running = True
        self.initialize_database()
        self.get_players_from_db()
        self.get_tournaments_from_db()
        choix = self.view.prompt_principal_menu()
        while running:
            if choix == "1":
                choix = self.view.afficher_menu_tournoi()
            elif choix == "11":
                number = self.get_number_of_players()
                if number < 8:
                    print("Attention, Il n'y a pas suffisamment de joueurs "
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
                elements_player = self.view.add_player()
                self.create_player(elements_player)
                # serialized_player = self.serialized_player(detail)
                # self.add_player_to_db(serialized_player)
                choix = self.view.afficher_menu_joueur()
            elif choix == "22":
                players = self.get_players_from_db()
                listing = self.sort_players_by_names(players)
                self.view.affichage_liste_joueurs_alphabetique(listing)
                choix = self.view.afficher_menu_joueur()
            elif choix == "23":
                players = self.get_players_from_db()
                listing = self.sort_players_by_rank(players)
                self.view.affichage_liste_joueurs_classement(listing)
                choix = self.view.afficher_menu_joueur()
            elif choix == "24":
                choix = self.view.prompt_principal_menu()
            elif choix == "3":
                return False
            else:
                print("Ce choix n'existe pas, merci de ré-essayer")
                choix = self.view.prompt_principal_menu()
