"""Module provides a class that takes users Pokemon's ability query and store it in an ability class object"""
from pokeretriever.poke_dex_object import PokeDexObject


class Ability(PokeDexObject):
    """
    Ability class is used to store pokemon's ability and used to send the data to console or output file and
    is a part of Pokemon's expanded output.
    """
    def __init__(self, generation, effect, pokemon, *args):
        """
        Initialize the data attributes of an ability object.

        :param generation: string
        :param effect: string
        :param pokemon: string list of Pokemon names
        :param args: string name, int id passed into PokeDexObject
        """
        super().__init__(*args)
        self._generation = generation
        self._effect = effect
        self._pokemon = pokemon

    def __str__(self):
        """
        Method used to return a Pokemon's ability and its specified attributes.

        :return: String of formatted ability specified attributes.
        """

        entry_string = ""
        entry_short_string = ""
        pokemon_names = []

        # Only grabbing english effect and short_effect description.
        for entry in self._effect:
            if entry['language']['name'] == "en":
                entry_string = entry['effect']
                entry_short_string = entry['short_effect']
                break

        # Grabbing pokemon names and storing it in a list
        for pokemon_name in self._pokemon:
            pokemon_names.append(pokemon_name['pokemon']['name'])

        pokemons = ", ".join(pokemon_names)

        return (super().__str__() +
                f"Generation: {self._generation}\n"
                f"Effect: {entry_string}\n"
                f"EFFECT (Short): {entry_short_string}\n"
                f"POKEMON: {pokemons}\n")
