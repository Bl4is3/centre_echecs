"""Base view"""



class View:
    """creation des vues"""

    def add_player(self):
        print(
            "-------------------------------\n"
            "Ajouter un joueur:\n"
            "-------------------------------\n"
        )

        first_name = input("Prénom du joueur :")
        last_name = input("Nom du joueur :")
        sex = input("H ou F :")
        date_birthday = input("Date de naissance :")
        rank = input("Classement :")
        details = [first_name, last_name, sex, date_birthday, rank]
        return details

    def afficher_menu_joueur(self):
        print(
            "-------------------------------\n"
            "Menu Joueur:\n"
            "-------------------------------\n"
            "21 - Ajouter un joueur \n"
            "22 - Afficher la liste des joueurs par alphabétique\n"
            "23 - Afficher la liste des joueurs par classement\n"
            "24 - Revenir au menu principal\n"
            "25 - Sauvegarder et quitter\n"
        )
        choix = input("Entrez votre choix :")
        return choix

    def prompt_principal_menu(self):
        print(
            "-------------------------------\n"
            "BIENVENUE AU CENTRE D'ECHECS:\n"
            "-------------------------------\n"
            "Menu Principal:\n"
            "-------------------------------\n"
            "1 - Menu Tournoi \n"
            "2 - Menu Joueur\n"
            "3 - Sauvegarder et quitter\n"
        )
        choix = input("Entrez votre choix :")
        return choix

    def afficher_menu_tournoi(self):
        print(
            "-------------------------------\n"
            "Menu Tournoi:\n"
            "-------------------------------\n"
            "11 - Créer un tournoi \n"
            "12 - Reprendre un tournoi en cours\n"
            "13 - Afficher la liste de tous les tournois \n"
            "14 - Afficher la liste de tous les tours d'un tournoi\n"
            "15 - Afficher la liste de tous les matchs d'un tournoi\n"
            "16 - Revenir au menu principal\n"
            "17 - Sauvegarder et quitter\n"
        )

        choix = input("Entrez votre choix :")
        return choix

    def affichage_liste_joueurs_alphabetique(self, players):
        self.players = players
        for player in players:
            print(player)

    def affichage_liste_joueurs_classement(self):
        self.afficher_menu_joueur()
