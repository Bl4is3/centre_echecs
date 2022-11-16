"""Define the main controller."""

from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.database import Database
from views.view import View
from tinydb import Query, where

from datetime import datetime


class Controller:
    """Main controller."""

    def __init__(self):
        """Has a a view."""
        # models
        self.view = View()
        self.db = Database('db.json')
    
    def create_player(self, detail):
        """ Instance a new player"""
        first_name = detail[0]
        last_name = detail[1]
        sex = detail[2]
        date_birthday = detail[3]
        rank = detail[4]
        id = self.db.get_last_id('players') + 1
        player = Player(id, first_name, last_name, sex,
                        date_birthday, rank)
        serialized_player = player.serialized_player(player)
        self.db.add_player_to_db(serialized_player)
    
    def unserialized_player(self, serialized_player):
        """Unserialize a player"""
        id = serialized_player['id']
        first_name = serialized_player['first_name']
        last_name = serialized_player['last_name']
        sex = serialized_player['sex']
        date_birthday = serialized_player['date_birthday']
        rank = serialized_player['rank']

        return Player(
            id,
            first_name,
            last_name,
            sex,
            date_birthday,
            rank)

    def create_tournament(self, detail):
        name = detail[0]
        place = detail[1]
        dates = detail[2]
        players = detail[3]
        timer = detail[4]
        description = detail[5]
        number_of_rounds = detail[6]
        scores = [0,0,0,0,0,0,0,0]
        rounds_ok = 0
        id = self.db.get_last_id('tournaments') + 1
        tournament = Tournament(
            id,
            name,
            place,
            dates,
            players,
            scores,
            timer,
            description,
            number_of_rounds, 
            rounds_ok
            )
        serialized_tournament = tournament.serialized_tournament(tournament)
        self.db.add_tournament_to_db(serialized_tournament)

        return tournament

    def unserialized_tournament(self, serialized_tournament):
        """ Instance a new player"""
        id = serialized_tournament['id']
        name = serialized_tournament['name']
        place = serialized_tournament['place']
        dates = serialized_tournament['dates']
        players = serialized_tournament['players']
        scores = serialized_tournament['scores']
        timer = serialized_tournament['timer']
        description = serialized_tournament['description']
        number_of_rounds = serialized_tournament['number_of_rounds']
        rounds_ok = serialized_tournament['rounds_ok']
        finished = serialized_tournament['finished']

        return Tournament(
            id,
            name,
            place,
            dates,
            players,
            scores,
            timer,
            description,
            number_of_rounds,
            rounds_ok,
            finished)
    
    def create_first_round(self, tournament_id):
        """Create first round"""
        name = 'Round_1'
        datetime_beginning = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        id = self.db.get_last_id('rounds') + 1
        round = Round(id, 1, tournament_id, datetime_beginning)
        serialized_round = round.serialized_round(round)
        self.db.add_round_to_db(serialized_round)

        return round

    def create_other_round(self, round_number, tournament_id):
        """Create other round"""
        name = 'Round_' + round_number
        datetime_beginning = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        id = self.db.get_last_id('rounds') + 1
        round = Round(id, round_number, tournament_id, datetime_beginning)
        serialized_round = round.serialized_round(round)
        self.db.add_round_to_db(serialized_round)

        return round

    def unserialized_round(self, serialized_round):
        """Unserialize a round"""
        id = serialized_round['id']
        number = serialized_round['number']
        id_tournament = serialized_round['id_tournament']
        datetime_beginning = serialized_round['datetime_beginning']
        datetime_end = serialized_round['datetime_end']

        return Round(
            id,
            number,
            id_tournament,
            datetime_beginning,
            datetime_end)  
    
    def load_tournament(self, id_tournament):
        tournaments = self.db.get_elements_from_db('tournaments')
        for tournament in tournaments:
            if tournament['id'] == int(id_tournament):
                unserialized_tournament = self.unserialized_tournament(tournament)
        if unserialized_tournament.rounds_ok == 0:
            self.create_first_round(unserialized_tournament.id)
        else:
            self.create_other_round(unserialized_tournament.rounds_ok, )
        unserialized_tournament.rounds_ok += 1
        print("Round n°: ", unserialized_tournament.rounds_ok, " en cours: " )


    def get_list_tournaments_not_finished(self):
        """ Get tournaments in progress"""
        all_tournaments = self.db.table('tournaments')
        list_tournaments = Query()
        tournaments_in_progress = all_tournaments.search(
            list_tournaments.finished == 'False')
        tournaments = []
        for tournament in tournaments_in_progress:
            unserialized_tournament = self.unserialized_tournament(tournament)
            tournaments.append(unserialized_tournament)
        return tournaments

    def sort_players_by_names(self, players):
        names = []
        for player in players:
            names.append(player[0]['last_name'])
        sorted_names = sorted(names)
        sorted_player_by_names = []
        for name in sorted_names:
            for player in players:
                if name == player[0]['last_name']:
                    sorted_player_by_names.append(player)
        return sorted_player_by_names

    def sort_players_by_rank(self, players):
        ranks = []
        for player in players:
            unserialized_player = self.unserialized_player(player) 
            ranks.append(unserialized_player.rank)
        sorted_ranks = sorted(ranks)
        sorted_player_by_ranks = []
        list_id = []
        for rank in sorted_ranks:
            for player in players:
                unserialized_player = self.unserialized_player(player)
                if rank == unserialized_player.rank:    
                    if unserialized_player.id not in list_id:
                        sorted_player_by_ranks.append(unserialized_player)
                        list_id.append(unserialized_player.id)
        return sorted_player_by_ranks

    def run(self):
        """Run the game."""
        running = True
        self.db.initialize_database()        
        choix = self.view.prompt_principal_menu()
        while running:
            players = self.db.get_elements_from_db('players')
            tournaments = self.db.get_elements_from_db('tournaments')
            if choix == "1":
                choix = self.view.afficher_menu_tournoi()
            elif choix == "11":
                number = self.db.get_number_of_players()
                if number < 8:
                    print("Attention, Il n'y a pas suffisamment de joueurs "
                          "inscrits pour débuter un tournoi")
                    choix = self.view.afficher_menu_joueur()
                else:
                    elements_tournament = self.view.create_tournament()
                    tournament = self.create_tournament(elements_tournament) 
                    self.create_first_round(tournament.id)
                                     
                    choix = self.view.afficher_menu_tournoi()
            elif choix == "12":
                id_tournament = self.view.select_tournament()
                self.load_tournament(id_tournament)
            elif choix == "13":                
                list_tournaments = []
                for tournament in tournaments:
                    unserialized_tournament = self.unserialized_tournament(tournament)
                    list_tournaments.append(unserialized_tournament)
                if not list_tournaments:
                    print('\nIl n\'y a encore aucun tournoi d\'enregistré!' )
                else:
                    self.view.show_listing_all_tournaments(list_tournaments)
                choix = self.view.afficher_menu_tournoi()
            elif choix == "16":
                choix = self.view.prompt_principal_menu()
            elif choix == "15":
                return False
            elif choix == "2":
                choix = self.view.afficher_menu_joueur()
            elif choix == "21":
                elements_player = self.view.add_player()
                self.create_player(elements_player)
                choix = self.view.afficher_menu_joueur()
            elif choix == "22":
                list_players = []
                for player in players:
                   unserialized_player = self.unserialized_player(player) 
                   list_players.append(unserialized_player)
                listing = self.sort_players_by_names(list_players)
                self.view.affichage_liste_joueurs_alphabetique(listing)
                choix = self.view.afficher_menu_joueur()
            elif choix == "23":
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
