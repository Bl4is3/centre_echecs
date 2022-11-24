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
        players = self.db.get_table_from_db('players')
        player = players.search(where('id') == elements[0])
        player[0][elements[1]] = elements[2]
        print('pl:', player)
        self.db.update_element('players', elements[1], elements[2], elements[0])

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
                (unserialized_tournament.players[i], unserialized_tournament.scores[i], unserialize_player.rank)
            )
        sorted_players = sorted(players_score_rank, key=itemgetter(1, 2), reverse=True)
        return sorted_players

    def load_tournament(self, id_tournament):
        tournaments = self.db.get_table_from_db("tournaments")
        tournament = tournaments.search(where("id") == id_tournament)
        unserialized_tournament = self.unserialize_tournament(tournament[0])
        rounds = unserialized_tournament.rounds
        list_rounds = []
        for round in rounds:
            list_rounds.append(round)
        players = self.db.get_table_from_db("players")
        result = True
        list_players = []
        for player in players:
            if player["id"] in unserialized_tournament.players:
                list_players.append(player)

        if not unserialized_tournament.rounds:
            round = self.create_round('Round_1')
            sorted_players = self.sort_players_rank_name(list_players)
            list_matchs = []
            for i in range(1, 5):
                id_player_1 = sorted_players[i - 1].id
                id_player_2 = sorted_players[i + 3].id
                result_player_1 = result_player_2 = ""
                match = ([id_player_1, result_player_1], [id_player_2, result_player_2])
                list_matchs.append(match)
                round.matchs = list_matchs

        elif len(unserialized_tournament.rounds) <= unserialized_tournament.number_of_rounds:
            previous_round = self.unserialize_round(rounds[len(unserialized_tournament.rounds)-1])
            previous_matchs = previous_round.matchs
            matchs_in_progress = []
            for previous_match in previous_matchs:
                if previous_match[0][1] == "":
                    matchs_in_progress.append(previous_match)
            if matchs_in_progress:
                round = previous_round
            else:
                name = 'Round_' + str(len(unserialized_tournament.rounds) + 1)
                list_matchs = []
                round = self.create_round(name)
                sorted_players = self.sorted_by_score_rank(unserialized_tournament.id)
                all_matchs = []
                for r in rounds:
                    unserialize_round = self.unserialize_round(r)
                    matchs = unserialize_round.matchs
                    for match in matchs:
                        all_matchs.append(match)
                already_play = []
                for match in all_matchs:
                    already_play.append((match[0][0], match[1][0]))
                a = 0
                b = 1
                while len(sorted_players) >= 2:
                    paire = (sorted_players[a][0], sorted_players[b][0])
                    if paire not in already_play:
                        match = ([sorted_players[a][0], ""], [sorted_players[b][0], ""])
                        list_matchs.append(match)
                        round.matchs = list_matchs
                        sorted_players.remove(sorted_players[a])
                        sorted_players.remove(sorted_players[b - 1])
                        b = 1
                    else:
                        if b < len(players) - 1:
                            b += 1
                        else:
                            a += 1
                            b = a + 1
        print("\n", round)
        print("\nVoici la liste des prochains matchs:\n")
        round_matchs = round.matchs
        for i in range(0, 4):
            print("Joueur n°:",  round.matchs[i][0][0], "/ Joueur n°:", round.matchs[i][1][0])
        for round_match in round_matchs:
            if round_match[0][1] == "":
                result = self.view.enter_match_winner(round_match)
                match_list = list(round_match)
                if result == "1":
                    score_indice = unserialized_tournament.players.index(round_match[0][0])
                    match_list[0][1] = 1
                    match_list[1][1] = 0
                    unserialized_tournament.scores[score_indice] += 1
                elif result == "2":
                    score_indice = unserialized_tournament.players.index(round_match[1][0])
                    match_list[0][1] = 0
                    match_list[1][1] = 1
                    unserialized_tournament.scores[score_indice] += 1
                elif result == "E":
                    score_indice_1 = unserialized_tournament.players.index(round_match[0][0])
                    unserialized_tournament.scores[score_indice_1] += 0.5
                    score_indice_2 = unserialized_tournament.players.index(round_match[1][0])
                    unserialized_tournament.scores[score_indice_2] += 0.5
                    match_list[0][1] = match_list[1][1] = 0.5
                elif result == "Q":
                    result = False
                    return
                round_match = tuple(match_list)
        round.matchs = round_matchs
        if len(round_matchs) == 4:
            round.datetime_end = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        serialized_round = round.serialize()
        list_rounds.append(serialized_round)
        unserialized_tournament.rounds = list_rounds
        tournaments.update({"scores": unserialized_tournament.scores}, where("id") == id_tournament)
        tournaments.update({"rounds": unserialized_tournament.rounds}, where("id") == id_tournament)
        if len(unserialized_tournament.rounds) == unserialized_tournament.number_of_rounds:
            unserialized_tournament.finished = True
            tournaments.update({"finished": unserialized_tournament.finished}, where("id") == id_tournament)
            print("\nLe tournoi est terminé")
            tournament_result = self.sorted_by_score_rank(id_tournament)
            self.view.show_tournament_result(tournament_result)
            result = False

        return result

    def get_list_tournaments_in_progress(self):
        """Get tournaments in progress"""
        tournaments = self.db.get_table_from_db("tournaments")
        tournaments_in_progress = tournaments.search(where("finished") == False)
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
                    self.view.show_listing_all_tournaments(list_tournaments)
                choix = self.view.show_tournament_menu()
            elif choix == "14":
                id_tournament = self.view.select_tournament()
                rounds = self.get_tournament_rounds(id_tournament)
                if not rounds:
                    print("\nIl n'y aucun tours démarrés dans ce tournoi")
                self.view.show_listing_all_rounds_of_a_tournament(rounds, id_tournament)
                choix = self.view.show_tournament_menu()
            elif choix == "15":
                id_tournament = self.view.select_tournament()
                rounds = self.get_tournament_rounds(id_tournament)
                self.view.show_listing_all_matchs_of_a_tournament(rounds, id_tournament)
                choix = self.view.prompt_principal_menu()
            elif choix in ("17", "3", "26"):
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
            elif choix == "25" or "16":
                choix = self.view.prompt_principal_menu()
            else:
                print("Ce choix n'existe pas, merci de ré-essayer")
                choix = self.view.prompt_principal_menu()
