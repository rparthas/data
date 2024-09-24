class User(object):

    def __init__(self, name, address, favorite_number, favorite_color):
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color
        # address should not be serialized, see user_to_dict()
        self._address = address


def __str__(self):
    return f"User(name={self.name}, address={self.address}, favorite_number={self.favorite_number}, favorite_color={self.favorite_color})"
