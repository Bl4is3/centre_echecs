"""Define the main controller."""
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from models.database import Database
from views.view import View
from tinydb import where
from operator import itemgetter

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
        self.db.add_element_to_db(player, "players")

    def unserialize_player(self, serialized_player):
        """Unserialize a player"""
        id = serialized_player["id"]
        first_name = serialized_player["first_name"]
        last_name = serialized_player["last_name"]
        sex = serialized_player["sex"]
        date_birthday = serialized_player["date_birthday"]
        rank = serialized_player["rank"]

        return Player(id, first_name, last_name, sex, date_birthday, rank)

    def unserialize_players(self, elements):
        unserialized_players = []
        for element in elements:
            unserialized_players.append(self.unserialize_player(element))
        return unserialized_players

    def create_tournament(self, detail):
        """ Create a tournament"""
        # à ajouter 
        # Doit egalement contenir une liste des rounds
        name = detail[0]
        place = detail[1]
        dates = detail[2]
        players = detail[3]
        timer = detail[4]
        description = detail[5]
        number_of_rounds = detail[6]
        scores = [0, 0, 0, 0, 0, 0, 0, 0]
        rounds_ok = 0 # peut etre ajouter la liste des rounds et itérer su longueur)
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
        self.db.add_element_to_db(tournament, "tournaments")

        return tournament

    def unserialize_tournament(self, serialized_tournament):
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

    def unserialize_tournaments(self, elements):
        unserialized_tournaments = []
        for element in elements:
            unserialized_tournaments.append(self.unserialize_tournament(element))
        return unserialized_tournaments

    def create_round(self, round_name, tournament_id):
        """Create other round"""
        # à ajouter 
        # un round doit contenir la liste des matchs
        datetime_beginning = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        id_round = self.db.get_last_id("rounds") + 1
        round = Round(id_round, round_name, tournament_id, datetime_beginning)
        self.db.add_element_to_db(round, "rounds")

        return id_round

    def unserialize_round(self, serialized_round):
        """Unserialize a round"""
        id = serialized_round["id"]
        name = serialized_round["name"]
        id_tournament = serialized_round["id_tournament"]
        datetime_beginning = serialized_round["datetime_beginning"]
        datetime_end = serialized_round["datetime_end"]

        return Round(id, number, id_tournament, datetime_beginning, datetime_end)

    def unserialize_rounds(self, elements):
        unserialized_rounds = []
        for element in elements:
            unserialized_rounds.append(self.unserialize_round(element))
        return unserialized_rounds

    def unserialize_match(self, serialized_match):
        """Unserialize a match"""
        id = serialized_match["id"]
        id_round = serialized_match["id_round"]
        id_player_1 = serialized_match["id_player_1"]
        id_player_2 = serialized_match["id_player_2"]
        result_player_1 = serialized_match["result_player_1"]
        result_player_2 = serialized_match["result_player_2"]

        return Match(id, id_round, id_player_1, id_player_2, result_player_1, result_player_2)

    def unserialize_matchs(self, elements):
        unserialized_matchs = []
        for element in elements:
            unserialized_matchs.append(self.unserialize_match(element))
        return unserialized_matchs

    def get_tournament_rounds(self, id_tournament):
        rounds = self.db.get_table_from_db("rounds")
        tournament_rounds = rounds.search(where("id_tournament") == id_tournament)
        return tournament_rounds

    def get_round_matchs(self, id_round):
        matchs = self.db.get_table_from_db("matchs")
        round_matchs = matchs.search(where("id_round") == id_round)
        return round_matchs

    def sorted_by_score_rank(self, id_tournament):
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        players = self.db.get_table_from_db("players")
        players_score_rank = []
        for i in range(0, 8):
            player = players.search(where("id") == unserialized_tournament.players[i])
            unserialize_player = self.unserialize_player(player[0])
            players_score_rank.append(
                (unserialized_tournament.players[i], unserialized_tournament.scores[i], unserialize_player.rank)
            )
        sorted_players = sorted(players_score_rank, key=itemgetter(1, 2), reverse=True)
        return sorted_players

    def load_tournament(self, id_tournament):
        # remplacer le round_number par le nom de round
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        players = self.db.get_table_from_db("players")
        rounds = self.db.get_table_from_db("rounds")
        matchs = self.db.get_table_from_db("matchs")
        list_players = []
        for player in players:
            if player["id"] in unserialized_tournament.players:
                list_players.append(player)

        if unserialized_tournament.rounds_ok == 0:
            round_name = "Round_1"
            round_id = self.create_round(round_name, unserialized_tournament.id)
            sorted_players = self.sort_players_rank_name(list_players)
            for i in range(1, 5):
                id = self.db.get_last_id("matchs") + 1
                id_joueur_1 = sorted_players[i - 1].id
                id_joueur_2 = sorted_players[i + 3].id
                # un match doit etre un tuple de 2 listes (id_joueur, score_joueur)
                match = Match(id, round_id, id_joueur_1, id_joueur_2)
                self.db.add_element_to_db(match, "matchs")

        elif unserialized_tournament.rounds_ok <= unserialized_tournament.number_of_rounds:
            previous_round = rounds.search(
                (where("name") == unserialized_tournament.rounds_ok) & (where("id_tournament") == id_tournament)
            )
            unserialize_previous_round = self.unserialize_round(previous_round[0])
            previous_round_matchs = matchs.search(where("id_round") == unserialize_previous_round.id)
            unserialized_previous_round_matchs = self.unserialize_matchs(previous_round_matchs)
            matchs_in_progress = []
            for match in unserialized_previous_round_matchs:
                if match.result_player_1 == "":
                    matchs_in_progress.append(match)
            if matchs_in_progress:
                round_number = unserialized_tournament.rounds_ok
                result = self.load_round_tournament(id_tournament, round_number)

            else:
                if unserialized_tournament.rounds_ok == unserialized_tournament.number_of_rounds:
                    result = False
                    print("\nLe tournoi est terminé")
                else:
                    round_number = unserialized_tournament.rounds_ok + 1
                    round_id = self.create_round(round_number, unserialized_tournament.id)
                    sorted_players = self.sorted_by_score_rank(unserialized_tournament.id)
                    rounds = self.get_tournament_rounds(id_tournament)
                    all_matchs = []
                    for round in rounds:
                        matchs = self.get_round_matchs(round["id"])
                        for match in matchs:
                            all_matchs.append(match)
                    already_play = []
                    for match in all_matchs:
                        already_play.append((match["id_player_1"], match["id_player_2"]))
                    a = 0
                    b = 1
                    while len(sorted_players) >= 2:
                        paire = (sorted_players[a][0], sorted_players[b][0])
                        if paire not in already_play:
                            id = self.db.get_last_id("matchs") + 1
                            match = Match(id, round_id, sorted_players[a][0], sorted_players[b][0])
                            self.db.add_element_to_db(match, "matchs")
                            sorted_players.remove(sorted_players[a])
                            sorted_players.remove(sorted_players[b - 1])
                            b = 1
                        else:
                            if b < len(players) - 1:
                                b += 1
                            else:
                                a += 1
                                b = a + 1
                    result = self.load_round_tournament(id_tournament, round_number)

        else:

            return

        if result:
            tournaments.update({"rounds_ok": round_number}, where("id") == id_tournament)

        return result

    def load_round_tournament(self, id_tournament, round_number):

        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        rounds = self.db.get_table_from_db("rounds")
        round = rounds.search((where("number") == round_number) & (where("id_tournament") == id_tournament))
        result = True
        if round:
            unserialized_round = self.unserialize_round(round[0])
            print("\n", unserialized_round)
            print("\nVoici la liste des prochains matchs:")
            matchs = self.db.get_table_from_db("matchs")
            unserialized_matchs_round = []
            matchs_round = matchs.search(where("id_round") == unserialized_round.id)
            for i in range(0, 4):
                unserialized_match = self.unserialize_match(matchs_round[i])
                print(unserialized_match)
                unserialized_matchs_round.append(unserialized_match)
            for match_round in unserialized_matchs_round:
                if match_round.result_player_1 == "":
                    result = self.view.get_match_winner(match_round)
                    if result == "1":
                        score_indice = unserialized_tournament.players.index(match_round.id_player_1)
                        match_round.result_player_1 = 1
                        match_round.result_player_2 = 0
                        unserialized_tournament.scores[score_indice] += 1
                    elif result == "2":
                        score_indice = unserialized_tournament.players.index(match_round.id_player_2)
                        match_round.result_player_2 = 1
                        match_round.result_player_1 = 0
                        unserialized_tournament.scores[score_indice] += 1
                    elif result == "E":
                        score_indice_1 = unserialized_tournament.players.index(match_round.id_player_1)
                        unserialized_tournament.scores[score_indice_1] += 0.5
                        score_indice_2 = unserialized_tournament.players.index(match_round.id_player_2)
                        unserialized_tournament.scores[score_indice_2] += 0.5
                        match_round.result_player_2 = match_round.result_player_1 = 0.5
                    elif result == "Q":
                        result = False
                        return
                    matchs.update({"result_player_2": match_round.result_player_2}, where("id") == match_round.id)
                    matchs.update({"result_player_1": match_round.result_player_1}, where("id") == match_round.id)
            # ajouter l'enregistrement auto de l'heure de fin du round
            tournaments.update({"scores": unserialized_tournament.scores}, where("id") == id_tournament)
        if round_number == 4:
            tournaments.update({"finished": True}, where("id") == id_tournament)
            tournament_result = self.sorted_by_score_rank(id_tournament)
            self.view.show_tournament_result(tournament_result)
            result = False

        return result

    def get_list_tournaments_in_progress(self):
        """Get tournaments in progress"""
        tournaments = self.db.get_table_from_db("tournaments")
        tournaments_in_progress = tournaments.search(where("finished") is False)
        return tournaments_in_progress

    def sort_players_by_names(self, players):
        unserialized_players = self.unserialize_players(players)
        sorted_player_by_names = sorted(unserialized_players, key=lambda player: player.last_name)
        return sorted_player_by_names

    def sort_players_rank_name(self, players):
        unserialized_players = self.unserialize_players(players)
        sorted_players_rank_name = sorted(unserialized_players, key=lambda player: (player.rank, player.last_name))
        return sorted_players_rank_name

    def run(self):
        """Run the game."""

        self.db.initialize_database()
        choix = self.view.prompt_principal_menu()
        while True:
            players = self.db.get_table_from_db("players")
            tournaments = self.db.get_table_from_db("tournaments")
            if choix == "1":
                choix = self.view.show_tournament_menu()
            elif choix == "11":
                number = self.db.get_number_of_elements("players")
                if number < 8:
                    print("Attention, Il n'y a pas suffisamment de joueurs " "inscrits pour débuter un tournoi")
                    choix = self.view.show_player_menu()
                else:
                    elements_tournament = self.view.create_tournament()
                    tournament = self.create_tournament(elements_tournament)
                    self.create_round(tournament.id)
                    choix = self.view.show_tournament_menu()
            elif choix == "12":
                id_tournament = self.view.select_tournament()
                result = True
                while result:
                    result = self.load_tournament(id_tournament)
                choix = self.view.show_tournament_menu()

            elif choix == "13":
                list_tournaments = self.unserialize_tournaments(tournaments)
                if not list_tournaments:
                    print("\nIl n'y a encore aucun tournoi d'enregistré!")
                else:
                    for tournament in list_tournaments:
                        self.view.show_listing_all_tournaments(tournament)
                        if tournament.finished is True:
                            tournament_result = self.sorted_by_score_rank(tournament.id)
                            self.view.show_tournament_result(tournament_result)
                choix = self.view.show_tournament_menu()
            elif choix == "14":
                tournaments_in_progress = self.get_list_tournaments_in_progress()
                list_tournaments = self.unserialized_tournaments(tournaments_in_progress)
                if not list_tournaments:
                    print("\nIl n'y a pas de tournois en cours.")
                else:
                    self.view.show_listing_all_tournaments(list_tournaments)
                choix = self.view.show_tournament_menu()
            elif choix == "16":
                id_tournament = self.view.select_tournament()
                rounds = self.get_tournament_rounds(id_tournament)
                for round in rounds:
                    unserialized_round = self.unserialize_round(round)
                    matchs = self.get_round_matchs(unserialized_round.id)
                    unserialized_matchs = self.unserialized_matchs(matchs)
                    self.view.show_listing_all_matchs_of_a_round(unserialized_matchs)
                choix = self.view.prompt_principal_menu()
            elif choix == "15":
                id_tournament = self.view.select_tournament()
                rounds = self.get_tournament_rounds(id_tournament)
                if not rounds:
                    print("\nIl n'y aucun tours démarrés dans ce tournoi")
                unserialized_rounds = self.unserialized_rounds(rounds)
                self.view.show_listing_all_rounds_of_a_tournament(unserialized_rounds, id_tournament)
                choix = self.view.show_tournament_menu()
            elif choix == "18":
                return False
            elif choix == "2":
                choix = self.view.show_player_menu()
            elif choix == "21":
                elements_player = self.view.add_player()
                self.create_player(elements_player)
                choix = self.view.show_player_menu()
            elif choix == "22":
                listing = self.sort_players_by_names(players)
                self.view.show_players_by_names(listing)
                choix = self.view.show_player_menu()
            elif choix == "23":
                listing = self.sort_players_rank_name(players)
                self.view.show_players_by_ranks_names(listing)
                choix = self.view.show_player_menu()
            elif choix == "24" or "17":
                choix = self.view.prompt_principal_menu()
            elif choix == "3":
                return False
            else:
                print("Ce choix n'existe pas, merci de ré-essayer")
                choix = self.view.prompt_principal_menu()
