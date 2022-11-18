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
        serialized_player = player.serialized_player(player)
        self.db.add_element_to_db(serialized_player, 'players')

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
        serialized_tournament = tournament.serialized_tournament(tournament)
        self.db.add_element_to_db(serialized_tournament, 'tournaments')

        return tournament

    def unserialized_tournament(self, serialized_tournament):
        """Instance a new player"""
        id = int(serialized_tournament["id"])
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
        serialized_round = round.serialized_round(round)
        self.db.add_element_to_db(serialized_round, 'rounds')

        return id_round

    def create_other_round(self, round_number, tournament_id):
        """Create other round"""
        name = "Round_" + str(round_number)
        datetime_beginning = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        id_round = self.db.get_last_id("rounds") + 1
        round = Round(id_round, round_number, tournament_id, datetime_beginning)
        serialized_round = round.serialized_round(round)
        self.db.add_element_to_db(serialized_round, 'rounds')

        return id_round

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
        number = serialized_match["number"]
        id_round = serialized_match["id_round"]
        id_player_1 = serialized_match["id_player_1"]
        id_player_2 = serialized_match["id_player_2"]
        result_player_1 = serialized_match["result_player_1"]
        result_player_2 = serialized_match["result_player_2"]

        return Match(
            number, id_round, id_player_1, id_player_2, result_player_1, result_player_2
        )
    
    def unserialized_matchs(self, elements):
        unserialized_matchs = []
        for element in elements:
            unserialized_matchs.append(self.unserialized_match(element))
        return unserialized_matchs

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
            sorted_players = self.sort_players_by_rank(list_players)                                    
            for i in range (1, 5):
                number = i
                id_joueur_1 = sorted_players[i-1].id
                id_joueur_2 = sorted_players[i+3].id
                match = Match(number, round_id, id_joueur_1, id_joueur_2)
                serialized_match = match.serialized_match(match)
                self.db.add_element_to_db(serialized_match, 'matchs')
                self.load_round_tournament(unserialized_tournament.id, unserialized_tournament.rounds_ok)
                unserialized_tournament.rounds_ok += 1

        elif unserialized_tournament.rounds_ok >= (unserialized_tournament.number_of_rounds - 1):
            unserialized_tournament.finished = True
            print("\nCe tournoi est déjà terminé.")
            return 
               
        else:
            id_round = self.create_other_round(
                unserialized_tournament.rounds_ok, 
                unserialized_tournament.id
            )
        
        t = unserialized_tournament.rounds_ok
        print("t:", t)

        tournaments.update({'rounds_ok': t}, where('id') == id_tournament)
        return t
        # creer les matchs d'un autre round
    def load_round_tournament(self,id_tournament, round_number):

        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialized_tournament(tournament[0])
        rounds = self.db.get_table_from_db('rounds')
        round = rounds.search(where('number') == round_number - 1) & (where('id_tournament') == id_tournament)
        print("r:", round)
        unserialized_round = self.unserialized_round(round)
        print(unserialized_round)
        print("\n Voici la liste des prochains matchs:")
        matchs = self.db.get_table_from_db('matchs')
        matchs_round = []
        for match in matchs:
            if match['id_round'] == round['id']:
                unserialized_match = self.unserialized_match(match)
                print(unserialized_match)
                matchs_round.append(unserialized_match)
        for match_round in matchs_round:
            result = self.view.get_match_winner(match_round)
            if result == 1:
                score_indice = self.get_score_indice_for_player(match_round.id_player_1, unserialized_tournament.list_players)
                match_round.result_player_1 = 1
                matchs.update()
                print('scores[{score_indice}]')

                tournaments.update({'scores[{score_indice}]' : 1}, where('id') == id_tournament)
            elif result == 2:
                score_indice = self.get_score_indice_for_player(match_round.id_player_2, unserialized_tournament.list_players)
                tournaments.update({'scores[{score_indice}]' : 1}, where('id') == id_tournament)
            elif result == 'E':
                score_indice = self.get_score_indice_for_player(match_round.id_player_1, unserialized_tournament.list_players)
                tournaments.update({'scores[{score_indice}]' : 0.5}, where('id') == id_tournament)
                score_indice = self.get_score_indice_for_player(match_round.id_player_2, unserialized_tournament.list_players)
                tournaments.update({'scores[{score_indice}]' : 0.5}, where('id') == id_tournament)
            elif result == 'Q':
                return
        
                        
    def get_score_indice_for_player(self, id_player, list_players):
        for i in len(list_players)-1:
            if id_player == list_players[i]:
                score_indice = i
        return score_indice



    def get_list_tournaments_in_progress(self):
        """Get tournaments in progress"""
        tournaments = self.db.get_table_from_db("tournaments")
        tournaments_in_progress = tournaments.search(where('finished') != True)
        # for tournament in tournaments:
        #     if tournament["finished"] == False:
        #         unserialized_tournament = self.unserialized_tournament(
        #                                                     tournament
        #                                                     )
        #         tournaments_in_progress.append(unserialized_tournament)
        return tournaments_in_progress

    def get_list_elements(self, id, elements):
        """Get list elements from table with id """
        all_elements = self.db.get_table_from_db(elements)
        list_elements = all_elements.search(where(str(id)) == id)
        return list_elements

    def sort_players_by_names(self, players):
        names = []
        for player in players:
            unserialized_player = self.unserialized_player(player)
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
            players = self.db.get_table_from_db("players")
            tournaments = self.db.get_elements_from_db("tournaments")
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
                self.load_round_tournament(id_tournament, round_number)
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
                listing = self.sort_players_by_names(players)
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
