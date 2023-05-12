"""Module provides a class that takes users Pokemon query and store it in a pokemon class object"""
from pokeretriever.poke_dex_object import PokeDexObject


class Pokemon(PokeDexObject):
    """
    Pokemon class is used to store pokemon's data and used to send the data to console or output file.
    """
    def __init__(self, height, weight, stats, types, abilities, move, *args):
        """
        Initialize the data attributes of a pokemon object.

        :param height: int
        :param weight: int
        :param stats: list stat object
        :param types: string list
        :param abilities: list ability object
        :param move: list move object
        :param args: string name, int id passed into PokeDexObject
        """
        super().__init__(*args)
        self._height = height
        self._weight = weight
        self._stats = stats
        self._types = types
        self._abilities = abilities
        self._move = move

    def __str__(self):
        """
        Method used to return a Pokemon's specified attributes.

        :return: String of formatted pokemon's specified attributes.
        """
        abilities = "\n".join([ability.__str__() for ability in self._abilities])
        stats = "\n".join([stat.__str__() for stat in self._stats])
        move = "\n".join([move.__str__() for move in self._move])

        return (
                super().__str__() +
                f"Height: {self._height}\n"
                f"Weight: {self._weight}\n"
                f"Types: {self._types}\n"

                f"\nStats:\n"
                f"------\n"
                f"{stats}\n"

                f"\nAbilities:\n"
                f"------\n"
                f"{abilities}\n"

                f"\nMove:\n"
                f"------\n"
                f"{move}")
