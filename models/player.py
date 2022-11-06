class Player:
    def __init__(self, first_name, last_name, date_birthday, sex, rank):
        self.first_name = first_name
        self.last_name = last_name
        self.date_birthday = date_birthday
        self.sex = sex
        self.rank = rank

    def __str__(self):
        """Used in print."""
        return (
            f"{self.first_name} - {self.last_name} , {self.sex}, classé(e) "
            f"{self.rank}"
        )

    def __repr__(self):
        """Used in print."""
        return str(self)