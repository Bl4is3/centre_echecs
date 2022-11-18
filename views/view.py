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

    def afficher_menu_joueur(self):
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

    def afficher_menu_tournoi(self):
        print(
            "\n-------------------------------\n"
            "Menu Tournoi:\n"
            "-------------------------------\n"
            "\n11 - Créer un tournoi \n"
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

    def affichage_liste_joueurs_alphabetique(self, players):
        self.players = players
        print("\n")
        print("Voici la liste des joueurs par ordre alphabétique : \n")
        for player in players:
            print(player)

    def affichage_liste_joueurs_classement(self, players):
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
        print(
            "\n-------------------------------\n"
            "Créer un tournoi:\n"
            "-------------------------------\n"
        )
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

    def show_listing_all_tournaments(self, tournaments):
        self.tournaments = tournaments

        print("\nVoici la liste des tournois : \n")
        for tournament in tournaments:
            print(tournament)

    def show_listing_all_rounds_of_a_tournament(self, rounds, id_tournament):
        self.rounds = rounds

        print(
            "\nVoici la liste des rounds du tournoi n:°{self.id_tournament}}:\n"
        )
        for rounds in rounds:
            print(round)

    def show_listing_all_matchs_of_a_tournament(self, matchs, id_tournament):
        self.matchs = matchs
        self.id_tournament = id_tournament

        print(
            "\nVoici la liste des matchs du tournoi n:°{self.id_tournament}:\n"
        )
        for match in matchs:
            print(match)

    def get_match_winner(self, match):
        print(
            "Veuillez entrer le vainqueur du match{match.number}:\n"
        )
        choix = input(
            "(1: Joueur 1, 2: Joueur 2, E: égalité, Q: quitter et sauvagerder ):"
        )
        return choix