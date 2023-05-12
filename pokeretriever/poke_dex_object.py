"""Module provides a base class for all pokemon's mode. Modes are 'pokemon', 'ability', and 'move'."""


class PokeDexObject:
    """
    PokeDexObject class used as a base class as each mode API contains a pokemon's name and pokemon's ID.
    """
    def __init__(self, name, identity):
        """
        Initialize the data attributes of an PokeDexObject object.

        :param name: string
        :param identity: Int
        """
        self._name = name
        self._id = identity

    def __str__(self):
        """
        Method used to return a Pokemon's name and Pokemon's ID

        :return: String of Pokemon's name and Pokemon's ID
        """
        return (f"Name: {self._name}\n"
                f"ID: {self._id}\n")
