class Tournament:
    def __init__(
        self,
        name,
        place,
        dates,
        players,
        type_of_timer,
        description,
        state,
        number_of_rounds=4,
    ):
        self.name = name
        self.place = place
        self.dates = dates
        self.players = players
        self.type_of_timer = type_of_timer
        self.description = description
        self.state = state
        self.number_of_rounds = number_of_rounds

    def __str__(self):
        """Used in print."""
        return (
            f"Tournoi {self.name} du {self.dates[0]} ({self.state})"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)