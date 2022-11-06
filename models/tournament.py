class Tournament:
    def __init__(
        self,
        name,
        place,
        list_dates_tournament,
        list_players,
        type_of_timer,
        description,
        number_of_rounds=4,
    ):
        self.name = name
        self.place = place
        self.list_dates_tournament = list_dates_tournament
        self.list_players = list_players
        self.type_of_timer = type_of_timer
        self.description = description
        self.number_of_rounds = number_of_rounds

    def __str__(self):
        """Used in print."""
        return (
            f"Tournoi {self.name} du {self.list_dates_tournament[0]}"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)