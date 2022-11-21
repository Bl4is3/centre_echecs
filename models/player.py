class Player:
    def __init__(self, id, first_name, last_name, date_birthday, sex, rank):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_birthday = date_birthday
        self.sex = sex
        self.rank = rank

    def __str__(self):
        """Used in print."""
        return (
            f"{self.id} _ {self.last_name.upper()} {self.first_name.title()} classé(e) {self.rank}"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)

    def serialize(self):
        """Serialize a player"""
        serialized_player = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'sex': self.sex,
            'date_birthday': self.date_birthday,
            'rank': self.rank
        }
        return serialized_player
