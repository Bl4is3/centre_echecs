"""Define the main controller."""
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from models.database import Database
from views.view import View
from tinydb import TinyDB, Query, where

from datetime import datetime


class Controller:
    """Main controller."""

    def __init__(self):
        """Has a a view."""
        # models
        self.view = View()
        self.db = Database("db.json")

    def create_player(self, detail):
        """Instance a new player"""
        first_name = detail[0]
        last_name = detail[1]
        sex = detail[2]
        date_birthday = detail[3]
        rank = detail[4]
        id = self.db.get_last_id("players") + 1
        player = Player(id, first_name, last_name, sex, date_birthday, rank)
        self.db.add_element_to_db(player, 'players')

    def unserialized_player(self, serialized_player):
        """Unserialize a player"""
        id = serialized_player["id"]
        first_name = serialized_player["first_name"]
        last_name = serialized_player["last_name"]
        sex = serialized_player["sex"]
        date_birthday = serialized_player["date_birthday"]
        rank = serialized_player["rank"]

        return Player(id, first_name, last_name, sex, date_birthday, rank)
    
    def unserialized_players(self, elements):
        unserialized_players = []
        for element in elements:
            unserialized_players.append(self.unserialized_player(element))
        return unserialized_players

    def create_tournament(self, detail):
        name = detail[0]
        place = detail[1]
        dates = detail[2]
        players = detail[3]
        timer = detail[4]
        description = detail[5]
        number_of_rounds = detail[6]
        scores = [0, 0, 0, 0, 0, 0, 0, 0]
        rounds_ok = 0
        id = self.db.get_last_id("tournaments") + 1
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
            rounds_ok,
        )
        self.db.add_element_to_db(tournament, 'tournaments')

        return tournament

    def unserialized_tournament(self, serialized_tournament):
        """Instance a new player"""
        id = serialized_tournament["id"]
        name = serialized_tournament["name"]
        place = serialized_tournament["place"]
        dates = serialized_tournament["dates"]
        players = serialized_tournament["players"]
        scores = serialized_tournament["scores"]
        timer = serialized_tournament["timer"]
        description = serialized_tournament["description"]
        number_of_rounds = serialized_tournament["number_of_rounds"]
        rounds_ok = serialized_tournament["rounds_ok"]
        finished = serialized_tournament["finished"]

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
            finished,
        )
    
    def unserialized_tournaments(self, elements):
        unserialized_tournaments = []
        for element in elements:
            unserialized_tournaments.append(self.unserialized_tournament(element))
        return unserialized_tournaments


    def create_first_round(self, tournament_id):
        """Create first round"""
        name = "Round_1"
        datetime_beginning = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        id_round = self.db.get_last_id("rounds") + 1
        round = Round(id_round, 1, tournament_id, datetime_beginning)
        self.db.add_element_to_db(round, 'rounds')

        return id_round

    def create_other_round(self, round_number, tournament_id):
        """Create other round"""
        name = "Round_" + str(round_number)
        datetime_beginning = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        id_round = self.db.get_last_id("rounds") + 1
        round = Round(id_round, round_number, tournament_id, datetime_beginning)
        self.db.add_element_to_db(round, 'rounds')

        return name

    def unserialized_round(self, serialized_round):
        """Unserialize a round"""
        id = serialized_round["id"]
        number = serialized_round["number"]
        id_tournament = serialized_round["id_tournament"]
        datetime_beginning = serialized_round["datetime_beginning"]
        datetime_end = serialized_round["datetime_end"]

        return Round(
            id, number, id_tournament, datetime_beginning, datetime_end
        )
    
    def unserialized_rounds(self, elements):
        unserialized_rounds = []
        for element in elements:
            unserialized_rounds.append(self.unserialized_round(element))
        return unserialized_rounds

    def unserialized_match(self, serialized_match):
        """Unserialize a match"""
        id = serialized_match["id"]
        id_round = serialized_match["id_round"]
        id_player_1 = serialized_match["id_player_1"]
        id_player_2 = serialized_match["id_player_2"]
        result_player_1 = serialized_match["result_player_1"]
        result_player_2 = serialized_match["result_player_2"]

        return Match(
            id, id_round, id_player_1, id_player_2, result_player_1, result_player_2
        )
    
    def unserialized_matchs(self, elements):
        unserialized_matchs = []
        for element in elements:
            unserialized_matchs.append(self.unserialized_match(element))
        return unserialized_matchs

    def get_tournament_rounds(self, id_tournament):
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        rounds = self.db.get_table_from_db('rounds')
        tournament_rounds = rounds.search(where('id_tournament') == id_tournament )
        return tournament_rounds
    
    def get_round_matchs(self, id_round):
        matchs = self.db.get_table_from_db('matchs')
        round_matchs = matchs.search(where('id_round') == id_round)
        return round_matchs
            

    def load_tournament(self, id_tournament):
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialized_tournament(tournament[0])
        players = self.db.get_table_from_db('players') 
        list_players = []
        for player in players:
            if player['id'] in unserialized_tournament.players:
                list_players.append(player)
        if unserialized_tournament.rounds_ok == 0:
            # rounds = self.db.get_elements_from_db("rounds")
            # for round in rounds:
            #     if round['id_tournament'] == unserialized_tournament.id:
            #         round_in_progress = self.unserialized_round(round)
            round_id = self.create_first_round(unserialized_tournament.id)
            sorted_players = self.sort_players_rank_name(list_players)                                    
            for i in range (1, 5):
                id = self.db.get_last_id("matchs") + 1
                id_joueur_1 = sorted_players[i-1].id
                id_joueur_2 = sorted_players[i+3].id
                match = Match(id, round_id, id_joueur_1, id_joueur_2)
                self.db.add_element_to_db(match, 'matchs')
            unserialized_tournament.rounds_ok += 1
            tournaments.update({'rounds_ok': unserialized_tournament.rounds_ok}, where('id') == id_tournament)
    
        elif unserialized_tournament.rounds_ok >= (unserialized_tournament.number_of_rounds - 1):
            unserialized_tournament.finished = True
            print("\nCe tournoi est déjà terminé.")
            unserialized_tournament.rounds_ok = 5
               
        else:
            name = self.create_other_round(
                unserialized_tournament.rounds_ok, 
                unserialized_tournament.id
            )
            print(name)
            unserialized_tournament.rounds_ok += 1
            tournaments.update({'rounds_ok': unserialized_tournament.rounds_ok}, where('id') == id_tournament)
            
        return unserialized_tournament.rounds_ok
            
    def load_round_tournament(self,id_tournament, round_number):

        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialized_tournament(tournament[0])
        rounds = self.db.get_table_from_db('rounds')
        round = rounds.search((where('number') == round_number ) & (where('id_tournament') == id_tournament))
        if round:
            unserialized_round = self.unserialized_round(round[0])
            print(unserialized_round)
            print("\nVoici la liste des prochains matchs:")
            matchs = self.db.get_table_from_db('matchs')
            unserialized_matchs_round =[]
            matchs_round = matchs.search(where('id_round') == unserialized_round.id)
            for i in range(0, 4):
                    unserialized_match = self.unserialized_match(matchs_round[i])
                    print(unserialized_match)
                    unserialized_matchs_round.append(unserialized_match)
            for match_round in unserialized_matchs_round:
                result = self.view.get_match_winner(match_round)
                if result == '1':
                    score_indice = unserialized_tournament.players.index(match_round.id_player_1)
                    match_round.result_player_1 = 1
                    matchs.update({'result_player_1':1}, where('id') == match_round.id)
                    unserialized_tournament.scores[score_indice] += 1
                    tournaments.update({'scores' : unserialized_tournament.scores}, where('id') == id_tournament)
                elif result == '2':
                    score_indice = unserialized_tournament.players.index(match_round.id_player_2)
                    match_round.result_player_2 = 1
                    matchs.update({'result_player_2':1}, where('id') == match_round.id)
                    unserialized_tournament.scores[score_indice] += 1
                    tournaments.update({'scores' : unserialized_tournament.scores}, where('id') == id_tournament)
                elif result == 'E':
                    score_indice_1 = unserialized_tournament.players.index(match_round.id_player_1)
                    unserialized_tournament.scores[score_indice_1] += 0.5
                    score_indice_2 = unserialized_tournament.players.index(match_round.id_player_2)
                    unserialized_tournament.scores[score_indice_2] += 0.5
                    match_round.result_player_2 = match_round.result_player_1 = 0.5
                    tournaments.update({'scores' : unserialized_tournament.scores}, where('id') == id_tournament)
                elif result == 'Q':
                    return
        



    def get_list_tournaments_in_progress(self):
        """Get tournaments in progress"""
        tournaments = self.db.get_table_from_db("tournaments")
        tournaments_in_progress = tournaments.search(where('finished') != True)
        return tournaments_in_progress

    def get_list_elements(self, id, elements):
        """Get list elements from table with id """
        all_elements = self.db.get_table_from_db(elements)
        list_elements = all_elements.search(where(str(id)) == id)
        return list_elements

    def sort_players_by_names(self, players):
        unserialized_players = self.unserialized_players(players)
        sorted_player_by_names = sorted(
            unserialized_players, key = lambda player: player.last_name)
        return sorted_player_by_names
    
    def sort_players_rank_name(self, players):
        unserialized_players = self.unserialized_players(players)
        sorted_players_rank_name= sorted(
            unserialized_players, key=lambda player: (player.rank, player.last_name)
            )
        return sorted_players_rank_name

    def run(self):
        """Run the game."""
        running = True
        self.db.initialize_database()
        choix = self.view.prompt_principal_menu()
        while running:
            players = self.db.get_table_from_db("players")
            tournaments = self.db.get_table_from_db("tournaments")
            if choix == "1":
                choix = self.view.afficher_menu_tournoi()
            elif choix == "11":
                number = self.db.get_number_of_elements('players')
                if number < 8:
                    print(
                        "Attention, Il n'y a pas suffisamment de joueurs "
                        "inscrits pour débuter un tournoi"
                    )
                    choix = self.view.afficher_menu_joueur()
                else:
                    elements_tournament = self.view.create_tournament()
                    tournament = self.create_tournament(elements_tournament)
                    self.create_first_round(tournament.id)
                    choix = self.view.afficher_menu_tournoi()
            elif choix == "12":
                id_tournament = self.view.select_tournament()
                round_number = self.load_tournament(id_tournament)
                while round_number <= 4:
                    self.load_round_tournament(id_tournament, round_number)
                    round_number +=1
                choix = self.view.afficher_menu_tournoi()
            elif choix == "13":
                list_tournaments = self.unserialized_tournaments(tournaments)
                if not list_tournaments:
                    print("\nIl n'y a encore aucun tournoi d'enregistré!")
                else:
                    self.view.show_listing_all_tournaments(list_tournaments)
                choix = self.view.afficher_menu_tournoi()
            elif choix == "14":
                tournaments_in_progress = self.get_list_tournaments_in_progress()
                list_tournaments = self.unserialized_tournaments(tournaments_in_progress)
                if not list_tournaments:
                    print("\nIl n'y a pas de tournois en cours.")
                else:
                    self.view.show_listing_all_tournaments(list_tournaments)
                choix = self.view.afficher_menu_tournoi()
            elif choix == "16":
                id_tournament = self.view.select_tournament()
                rounds = self.get_tournament_rounds(id_tournament)
                for round in rounds:
                    unserialized_round = self.unserialized_round(round)
                    matchs = self.get_round_matchs(unserialized_round.id)
                    unserialized_matchs = self.unserialized_matchs(matchs)
                    self.view.show_listing_all_matchs_of_a_round(unserialized_matchs)
                choix = self.view.prompt_principal_menu()
            elif choix == '15':
                id_tournament = self.view.select_tournament()
                rounds = self.get_tournament_rounds(id_tournament)
                unserialized_rounds = self.unserialized_rounds(rounds)
                self.view.show_listing_all_rounds_of_a_tournament(unserialized_rounds, id_tournament)
                choix = self.view.afficher_menu_tournoi()
            elif choix == "18":
                return False
            elif choix == "2":
                choix = self.view.afficher_menu_joueur()
            elif choix == "21":
                elements_player = self.view.add_player()
                self.create_player(elements_player)
                choix = self.view.afficher_menu_joueur()
            elif choix == "22":
                listing = self.sort_players_by_names(players)
                self.view.affichage_liste_joueurs_alphabetique(listing)
                choix = self.view.afficher_menu_joueur()
            elif choix == "23":
                listing = self.sort_players_rank_name(players)
                self.view.affichage_liste_joueurs_classement(listing)
                choix = self.view.afficher_menu_joueur()
            elif choix == "24" or "17":
                choix = self.view.prompt_principal_menu()
            elif choix == "3":
                return False
            else:
                print("Ce choix n'existe pas, merci de ré-essayer")
                choix = self.view.prompt_principal_menu()
