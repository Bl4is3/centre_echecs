class Round:
    def __init__(self, id, number, id_tournament, datetime_beginning, datetime_end= None):
        self.id = id
        self.number = number
        self.id_tournament = id_tournament
        self.datetime_beginning = datetime_beginning
        self.datetime_end = datetime_end
    
    def __str__(self):
        """Used in print."""
        return (
            f"Round_{self.number} _ du tournoi n°: {self.id_tournament} qui a débuté le "
            f"{self.datetime_beginning} et a terminé le {self.datetime_end}"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialize(self):
        """Serialize a round"""
        serialized_round = {
            'id': self.id,
            'number': self.number,
            'id_tournament': self.id_tournament,
            'datetime_beginning': self.datetime_beginning,
            'datetime_end': self.datetime_end
        }
        return serialized_round

    