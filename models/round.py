class Round:
    def __init__(self, id, name, id_tournament, datetime_beginning, datetime_end=None):
        self.id = id
        self.name = name
        self.id_tournament = id_tournament
        self.datetime_beginning = datetime_beginning
        self.datetime_end = datetime_end

    def __str__(self):
        """Used in print."""
        return (
            f"Round_{self.number} du tournoi n°:{self.id_tournament} qui a débuté le "
            f"{self.datetime_beginning}"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialize(self):
        """Serialize a round"""
        serialized_round = {
            'id': self.id,
            'name': self.name,
            'id_tournament': self.id_tournament,
            'datetime_beginning': self.datetime_beginning,
            'datetime_end': self.datetime_end
        }
        return serialized_round
