from models.tournament import Tournament
from views.view import View
from controllers.base import Controller


def main():
    view = View()
    # debut.prompt_principal_menu()
    controller = Controller(view)
    controller.run()


if __name__ == "__main__":
    main()
