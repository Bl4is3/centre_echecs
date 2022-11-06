"""Base view"""
from controllers.base import Controller

class View:
    """creation des vues"""

    def add_player(self):
        print(
            "-------------------------------\n"
            "Ajouter un joueur:\n"
            "-------------------------------\n"
        )
        joueur = []
        nom = input("Nom du joueur :")
        joueur.append(nom)
        prenom = input("Prénom du joueur :")
        joueur.append(prenom)
        sexe = input("H ou F :")
        joueur.append(sexe)
        date_naissance = input("Date de naissance :")
        joueur.append(date_naissance)
        classement = input("Classement :")
        joueur.append(classement)
        self.afficher_menu_joueur()
        return joueur

    def afficher_menu_joueur(self):
        print(
            "-------------------------------\n"
            "Menu Joueur:\n"
            "-------------------------------\n"
            "1 - Ajouter un joueur \n"
            "2 - Afficher la liste des joueurs par alphabétique\n"
            "3 - Afficher la liste des joueurs par classement\n"
            "4 - Revenir au menu principal\n"
            "5 - Sauvegarder et quitter\n"
        )
        choix = input("Entrez votre choix :")
        if choix == "1":
            self.add_player()
        elif choix == "2":
            self.affichage_liste_joueurs_alphabetique()
        elif choix == "3":
            self.affichage_liste_joueurs_classement()
        elif choix == "4":
            self.prompt_principal_menu()
        elif choix == "5":
            return
        else:
            print("Ce choix n'existe pas, merci de recommencer")
            self.afficher_menu_joueur()

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
        if choix == "1":
            self.afficher_menu_tournoi()
        elif choix == "2":
            self.afficher_menu_joueur()
        else:
            print("Ce choix n'existe pas, merci de recommencer")
            self.prompt_principal_menu()

    def afficher_menu_tournoi(self):
        print(
            "-------------------------------\n"
            "Menu Tournoi:\n"
            "-------------------------------\n"
            "1 - Créer un tournoi \n"
            "2 - Afficher la liste de tous les tournois \n"
            "3 - Afficher la liste de tous les tours d'un tournoi\n"
            "4 - Afficher la liste de tous les matchs d'un tournoi\n"
            "5 - Revenir au menu principal\n"
            "6 - Sauvegarder et quitter\n"
        )
        choix = input("Entrez votre choix :")
        if choix == "1":
            self.begin_tournament()
        elif choix == "2":
            self.affichage_liste_tournois()
        elif choix == "3":
            self.affichage_liste_tours_d_un_tournoi()
        elif choix == "4":
            self.affichage_liste_matchs_d_un_tournoi()
        elif choix == "5":
            self.prompt_principal_menu()
        elif choix == "6":
            return
        else:
            print("Ce choix n'existe pas, merci de recommencer")
            self.afficher_menu_joueur()

    def affichage_liste_joueurs_alphabetique(self):
        print("coucou")
        self.afficher_menu_joueur()

    def affichage_liste_joueurs_classement(self):
        self.afficher_menu_joueur()
