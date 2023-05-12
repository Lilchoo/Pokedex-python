"""Module provides a class that takes users Pokemon's move query and store it in a move class object"""
from pokeretriever.poke_dex_object import PokeDexObject


class Move(PokeDexObject):
    """
    Move class is used to store pokemon's move(s) and used to send the data to console or output file and
    is a part of Pokemon's expanded output.
    """
    def __init__(self, generation, accuracy, pp, power, move_type, damage_class, effect, *args):
        """
        Initialize the data attributes of a move object.

        :param generation: String
        :param accuracy: Int
        :param pp: Int
        :param power: Int
        :param move_type: String
        :param damage_class: String
        :param effect: String
        :param args: string name, int id passed into PokeDexObject
        """
        super().__init__(*args)
        self._generation = generation
        self._accuracy = accuracy
        self._pp = pp
        self._power = power
        self._type = move_type
        self._damage_class = damage_class
        self._effect = effect

    def __str__(self):
        return (super().__str__() +
                f'Generation: {self._generation}\n'
                f'Accuracy: {self._accuracy}\n'
                f'PP: {self._pp}\n'
                f'Power: {self._power}\n'
                f'Type: {self._type}\n'
                f'Damage Class: {self._damage_class}\n'
                f'Effect (Short): {self._effect}')
