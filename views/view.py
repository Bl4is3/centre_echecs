"""Base view"""


class View:
    """creation des vues"""

    def add_player(self):
        print(
            "\n-------------------------------\n"
            "Ajouter un joueur:\n"
            "-------------------------------\n"
        )
        first_name = input("Prénom du joueur: ")
        last_name = input("Nom du joueur: ")
        sex = input("H ou F: ")
        date_birthday = input("Date de naissance: ")
        rank = input("Classement: ")

        elements_player = [first_name, last_name, sex, date_birthday, rank]
        return elements_player

    def show_player_menu(self):
        print(
            "\n-------------------------------\n"
            "Menu Joueur:\n"
            "-------------------------------\n"
            "\n21 - Ajouter un joueur \n"
            "22 - Afficher la liste des joueurs par alphabétique\n"
            "23 - Afficher la liste des joueurs par classement\n"
            "24 - Revenir au menu principal\n"
            "25 - Sauvegarder et quitter\n"
        )
        choix = input("Entrez votre choix :")
        return choix

    def prompt_principal_menu(self):
        print(
            "\n-------------------------------\n"
            "BIENVENUE AU CENTRE D'ECHECS:\n"
            "-------------------------------\n"
            "Menu Principal:\n"
            "-------------------------------\n"
            "\n1 - Menu Tournoi \n"
            "2 - Menu Joueur\n"
            "3 - Sauvegarder et quitter\n"
        )
        choix = input("Entrez votre choix :")
        return choix

    def show_tournament_menu(self):
        print(
            "\n-------------------------------\n"
            "Menu Tournoi:\n"
            "-------------------------------\n"
            "11 - Créer un tournoi \n"
            "12 - Lancer / Reprendre un tournoi \n"
            "13 - Afficher la liste de tous les tournois \n"
            "14 - Afficher la liste de tous les tournois en cours \n"
            "15 - Afficher la liste de tous les tours d'un tournoi\n"
            "16 - Afficher la liste de tous les matchs d'un tournoi\n"
            "17 - Revenir au menu principal\n"
            "18 - Sauvegarder et quitter\n"
        )

        choix = input("Entrez votre choix :")
        return choix

    def show_players_by_names(self, players):
        self.players = players
        print("\n")
        print("Voici la liste des joueurs par ordre alphabétique : \n")
        for player in players:
            print(player)

    def show_players_by_ranks_names(self, players):
        self.players = players

        print("\nVoici la liste des joueurs par classemnt croissant : \n")
        for player in players:
            print(player)

    def create_list_player_tournament(self):
        player_1 = int(input("Id du joueur 1: "))
        player_2 = int(input("Id du joueur 2: "))
        player_3 = int(input("Id du joueur 3: "))
        player_4 = int(input("Id du joueur 4: "))
        player_5 = int(input("Id du joueur 5: "))
        player_6 = int(input("Id du joueur 6: "))
        player_7 = int(input("Id du joueur 7: "))
        player_8 = int(input("Id du joueur 8: "))
        players = [
            player_1,
            player_2,
            player_3,
            player_4,
            player_5,
            player_6,
            player_7,
            player_8,
        ]

        return players

    def create_tournament(self):
        print("\n-------------------------------\n" "Créer un tournoi:\n" "-------------------------------\n")
        name = input("Nom du tournoi: ")
        place = input("Lieu du tournoi: ")
        date_beginning = input("Date du 1er jour: ")
        players = self.create_list_player_tournament()
        timer = input("Choix du timer (1:bullet / 2:blitz / 3:coup rapide): ")
        description = input("Description: ")
        number_of_rounds = int(input("Nb de tours ( 4 par défault )"))
        details = [
            name,
            place,
            date_beginning,
            players,
            timer,
            description,
            number_of_rounds,
        ]
        return details

    def select_tournament(self):
        id_tournament = int(input("\nEntrez un numéro du tournoi: "))
        return id_tournament

    def show_listing_all_tournaments(self, tournament):
        self.tournament = tournament
        print(tournament)

    def show_listing_all_rounds_of_a_tournament(self, rounds, id_tournament):
        self.rounds = rounds
        self.id_tournament = id_tournament

        print("\nVoici la liste des rounds du tournoi n:°", self.id_tournament, ":\n")
        for round in rounds:
            print(round)

    def show_listing_all_matchs_of_a_round(self, matchs):
        self.matchs = matchs
        for match in matchs:
            print(match)

    def show_tournament_result(self, tournament_result):
        self.tournament_result = tournament_result
        print("Résultat:")
        print("Vainqueur: Joueur", tournament_result[0][0], " avec ", tournament_result[0][1], "points")
        print("Second: Joueur", tournament_result[1][0], " avec ", tournament_result[1][1], "points")
        for i in range(2, 8):
            print("", i + 1, "ème: Joueur", tournament_result[i][0], " avec ", tournament_result[i][1], "points")

    def get_match_winner(self, match):
        self.match = match
        print("\nVeuillez entrer le vainqueur du ", match, ": ")
        choix = input("Joueur (1), Joueur (2), (E)galité, (Q)uitter:")
        return choix
