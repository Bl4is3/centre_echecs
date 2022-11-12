class Tournament:
    def __init__(
        self,
        id,
        name,
        place,
        date_beginning,
        players,
        timer,
        description,
        finished=False,
        number_of_rounds=4,
    ):
        self.id = id
        self.name = name
        self.place = place
        self.date_beginning = date_beginning
        self.players = players
        self.timer = timer
        self.description = description
        self.finished = finished
        self.number_of_rounds = number_of_rounds

    def __str__(self):
        """Used in print."""
        return (
            f"{self.id} _ Tournoi {self.name} du {self.date_beginning} ({self.finished})"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)
