"""Module provides a class that takes users Pokemon's stats query and store it in a Stat object"""
from pokeretriever.poke_dex_object import PokeDexObject


class Stat(PokeDexObject):
    """
    Stats class is used to store Pokemon's stats and used exclusively when it is in expanded mode as part of the
    query of a Pokemon.
    """
    def __init__(self, is_battle, *args):
        """
        Initialize the data attributes of a stat object.

        :param is_battle: boolean
        :param args: string name, int id passed into PokeDexObject
        """
        super().__init__(*args)
        self._is_battle = is_battle

    def __str__(self):
        """
        Method used to return a Pokemon's stat and its specified attribtues.

        :return: String of formatted stat specified attributes
        """
        return (super().__str__() +
                f'Is Battle Only: {self._is_battle}')

