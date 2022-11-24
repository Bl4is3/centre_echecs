class Round:
    def __init__(self, name, matchs, datetime_beginning, datetime_end=None):
        self.name = name
        self.matchs = matchs
        self.datetime_beginning = datetime_beginning
        self.datetime_end = datetime_end

    def __str__(self):
        """Used in print."""
        return (
            f"{self.name} qui a débuté le "
            f"{self.datetime_beginning}"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialize(self):
        """Serialize a round"""
        serialized_round = {
            'name': self.name,
            'matchs': self.matchs,
            'datetime_beginning': self.datetime_beginning,
            'datetime_end': self.datetime_end
        }
        return serialized_round
