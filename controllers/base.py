"""Define the main controller."""
from models.player import Player
from models.tournament import Tournament
from models.round import Round
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

    def modify_player(self, elements):
        """Modify a player"""
        players = self.db.get_table_from_db("players")
        player = players.search(where("id") == elements[0])
        player[0][elements[1]] = elements[2]
        print("pl:", player)
        self.db.update_element("players", elements[1], elements[2], elements[0])

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
        """Create a tournament"""
        name = detail[0]
        place = detail[1]
        dates = detail[2]
        players = detail[3]
        timer = detail[4]
        description = detail[5]
        number_of_rounds = detail[6]
        scores = [0, 0, 0, 0, 0, 0, 0, 0]
        rounds = []
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
            rounds,
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
        rounds = serialized_tournament["rounds"]
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
            rounds,
            finished,
        )

    def unserialize_tournaments(self, elements):
        unserialized_tournaments = []
        for element in elements:
            unserialized_tournaments.append(self.unserialize_tournament(element))
        return unserialized_tournaments

    def create_round(self, name):
        """Create other round"""
        datetime_beginning = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        matchs = []
        round = Round(name, matchs, datetime_beginning)
        return round

    def unserialize_round(self, serialized_round):
        """Unserialize a round"""
        name = serialized_round["name"]
        matchs = serialized_round["matchs"]
        datetime_beginning = serialized_round["datetime_beginning"]
        datetime_end = serialized_round["datetime_end"]

        return Round(name, matchs, datetime_beginning, datetime_end)

    def unserialize_rounds(self, elements):
        unserialized_rounds = []
        for element in elements:
            unserialized_rounds.append(self.unserialize_round(element))
        return unserialized_rounds

    def get_tournament_rounds(self, id_tournament):
        """Get all rounds of a tournament"""
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        unserialized_rounds = self.unserialize_rounds(unserialized_tournament.rounds)
        return unserialized_rounds

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
                (
                    unserialized_tournament.players[i],
                    unserialized_tournament.scores[i],
                    unserialize_player.rank,
                )
            )
        sorted_players = sorted(players_score_rank, key=itemgetter(1, 2), reverse=True)
        return sorted_players

    def verify_if_matchs_in_progress_in_round(self, round):
        previous_matchs = round.matchs
        result = False
        matchs_in_progress = []
        for previous_match in previous_matchs:
            if previous_match[0][1] == "":
                matchs_in_progress.append(previous_match)
        if matchs_in_progress:
            result = True
        return result

    def create_matchs_first_round(self, list_players):
        sorted_players = self.sort_players_rank_name(list_players)
        list_matchs = []
        for i in range(1, 5):
            id_player_1 = sorted_players[i - 1].id
            id_player_2 = sorted_players[i + 3].id
            result_player_1 = result_player_2 = ""
            match = ([id_player_1, result_player_1], [id_player_2, result_player_2])
            list_matchs.append(match)
        return list_matchs

    def create_matchs_other_round(self, round, id_tournament):
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        rounds = unserialized_tournament.rounds
        sorted_players = self.sorted_by_score_rank(id_tournament)
        list_matchs = []
        all_matchs = []
        for r in rounds:
            unserialize_round = self.unserialize_round(r)
            matchs = unserialize_round.matchs
            for match in matchs:
                all_matchs.append(match)
        already_play = [(match[0][0], match[1][0]) for match in all_matchs]
        a = 0
        b = 1

        while len(sorted_players) >= 2:
            paire = (sorted_players[a][0], sorted_players[b][0])
            if paire not in already_play or len(sorted_players) == 2:
                match = ([sorted_players[a][0], ""], [sorted_players[b][0], ""])
                round.matchs = list_matchs.append(match)
                sorted_players.remove(sorted_players[a])
                sorted_players.remove(sorted_players[b - 1])
                b = 1
            else:
                b += 1
        return list_matchs

    def load_tournament(self, id_tournament):
        ended = False
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        rounds = unserialized_tournament.rounds
        players = self.db.get_table_from_db("players")
        resultat = True
        list_players = []
        for player in players:
            if player["id"] in unserialized_tournament.players:
                list_players.append(player)
        if not unserialized_tournament.rounds:
            round = self.create_round("Round_1")
            list_matchs = self.create_matchs_first_round(list_players)
            round.matchs, scores, resultat = self.run_matchs_round("Round_1", list_matchs, unserialized_tournament.id)
            serialized_round = round.serialize()
            rounds.append(serialized_round)
        elif len(unserialized_tournament.rounds) <= unserialized_tournament.number_of_rounds:
            round = self.unserialize_round(rounds[len(unserialized_tournament.rounds) - 1])
            result = self.verify_if_matchs_in_progress_in_round(round)
            if result:
                round.matchs, scores, resultat = self.run_matchs_round(
                    round.name, round.matchs, unserialized_tournament.id
                )
                serialized_round = round.serialize()
                rounds[len(unserialized_tournament.rounds) - 1] = serialized_round
            else:
                if len(unserialized_tournament.rounds) == unserialized_tournament.number_of_rounds and not result:
                    unserialized_tournament.finished = True
                    tournaments.update({"finished": unserialized_tournament.finished}, where("id") == id_tournament)
                    tournament_result = self.sorted_by_score_rank(id_tournament)
                    self.view.show_tournament_result(tournament_result)
                    resultat = False
                    ended = True
                else:
                    name = "Round_" + str(len(unserialized_tournament.rounds) + 1)
                    round = self.create_round(name)
                    list_matchs = self.create_matchs_other_round(round, unserialized_tournament.id)
                    round.matchs, scores, resultat = self.run_matchs_round(
                        name, list_matchs, unserialized_tournament.id
                    )
                    if len(round.matchs) == 4:
                        round.datetime_end = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    serialized_round = round.serialize()
                    rounds.append(serialized_round)
        if not ended:
            unserialized_tournament.rounds = rounds
            tournaments.update({"rounds": unserialized_tournament.rounds}, where("id") == id_tournament)
            tournaments.update({"scores": scores}, where("id") == id_tournament)
        return resultat

    def run_matchs_round(self, name_round, list_matchs, id_tournament):
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        print("\n", name_round, "\nVoici la liste des prochains matchs:\n")
        resultat = True
        for i in range(0, 4):
            print("Joueur n°:", list_matchs[i][0][0], "/ Joueur n°:", list_matchs[i][1][0])
        for match in list_matchs:
            if match[0][1] == "":
                result = self.view.enter_match_winner(match)
                if result == "1":
                    score_indice = unserialized_tournament.players.index(match[0][0])
                    match[0][1] = 1
                    match[1][1] = 0
                    unserialized_tournament.scores[score_indice] += 1
                elif result == "2":
                    score_indice = unserialized_tournament.players.index(match[1][0])
                    match[0][1] = 0
                    match[1][1] = 1
                    unserialized_tournament.scores[score_indice] += 1
                elif result == "E":
                    score_indice_1 = unserialized_tournament.players.index(match[0][0])
                    unserialized_tournament.scores[score_indice_1] += 0.5
                    score_indice_2 = unserialized_tournament.players.index(match[1][0])
                    unserialized_tournament.scores[score_indice_2] += 0.5
                    match[0][1] = match[1][1] = 0.5
                elif result == "Q":
                    resultat = False
                    return list_matchs, unserialized_tournament.scores, resultat
        return list_matchs, unserialized_tournament.scores, resultat

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

    def get_players_tournament(self, id_tournament):
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        players = self.db.get_table_from_db("players")
        print(players)
        list_players = []
        for player in unserialized_tournament.players:
            pl = players.search(where("id") == player)
            unserialized_player = self.unserialize_player(pl[0])
            list_players.append(unserialized_player)

        return list_players

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
                elements_tournament = self.view.create_tournament()
                self.create_tournament(elements_tournament)
                choix = self.view.show_tournament_menu()
            elif choix == "12":
                id_tournament = self.view.select_tournament()
                result = True
                while result:
                    result = self.load_tournament(id_tournament)
                choix = self.view.show_tournament_menu()
            elif choix == "13":
                list_tournaments = self.unserialize_tournaments(tournaments)
                for tournament in list_tournaments:
                    if tournament.finished:
                        print("\n", tournament)
                        tournament_result = self.sorted_by_score_rank(tournament.id)
                        self.view.show_tournament_result(tournament_result)
                    else:
                        print("\n", tournament)
                choix = self.view.show_tournament_menu()
            elif choix == "14":
                id_tournament = self.view.select_tournament()
                rounds = self.get_tournament_rounds(id_tournament)
                self.view.show_listing_all_rounds_of_a_tournament(rounds, id_tournament)
                choix = self.view.show_tournament_menu()
            elif choix == "15":
                id_tournament = self.view.select_tournament()
                rounds = self.get_tournament_rounds(id_tournament)
                self.view.show_listing_all_matchs_of_a_tournament(rounds, id_tournament)
                choix = self.view.prompt_principal_menu()
            elif choix == "16":
                id_tournament = self.view.select_tournament()
                list_player_tournament = self.get_players_tournament(id_tournament)
                list = sorted(list_player_tournament, key=lambda player: player.last_name)
                self.view.show_players_by_names(list)
                choix = self.view.prompt_principal_menu()
            elif choix == "17":
                id_tournament = self.view.select_tournament()
                list_player_tournament = self.get_players_tournament(id_tournament)
                list = sorted(list_player_tournament, key=lambda player: player.rank)
                self.view.show_players_by_names(list)
                choix = self.view.prompt_principal_menu()
            elif choix in ("19", "3", "26"):
                return False
            elif choix == "2":
                choix = self.view.show_player_menu()
            elif choix == "21":
                elements_player = self.view.add_player()
                self.create_player(elements_player)
                choix = self.view.show_player_menu()
            elif choix == "22":
                element_player = self.view.modify_player()
                self.modify_player(element_player)
                choix = self.view.show_player_menu()
            elif choix == "23":
                listing = self.sort_players_by_names(players)
                self.view.show_players_by_names(listing)
                choix = self.view.show_player_menu()
            elif choix == "24":
                listing = self.sort_players_rank_name(players)
                self.view.show_players_by_ranks_names(listing)
                choix = self.view.show_player_menu()
            elif choix == "25" or "18":
                choix = self.view.prompt_principal_menu()
            else:
                choix = self.view.prompt_principal_menu()
