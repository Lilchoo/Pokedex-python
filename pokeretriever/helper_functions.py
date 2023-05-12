import os.path

import aiohttp
import asyncio

from pokeretriever.ability import Ability
from pokeretriever.custom_exceptions import InvalidFileTypeError, FileExtensions
from pokeretriever.move import Move
from pokeretriever.stat import Stat
from pokeretriever.pokemon import Pokemon
from pathlib import Path


def read_file(path: str) -> list:
    """
    Read the input file line by line and store the values in a list that will be used for a Pokemon API call.

    :param path: string, location of where the file exists
    :return: string list.
    """
    try:
        # check file extension
        extension_suffix = Path(path).suffix
        if extension_suffix not in [file.value for file in FileExtensions]:
            raise InvalidFileTypeError(f'Invalid file type')

        # check file exits
        if not os.path.exists(path):
            raise FileNotFoundError()

        # read file and append value from each line into data_list
        data_list = []
        with open(path, 'r') as file:
            for line_value in file:
                data_list.append(line_value)

    except FileNotFoundError:
        print(f'Error message: File not found. Please try again.')
        exit()
    except ValueError:
        print(f'Error message: Your file is not of proper format. Please try again')
        exit()
    except InvalidFileTypeError:
        print(f'Error message: Cannot read invalid file type. Please try again')
        exit()

    else:
        return data_list


async def get_single_request(url: str, session: aiohttp.ClientSession) -> dict | None:
    """
    Method used when the input data argument is provided in the command line.

    :param url: str
    :param session: aiohttp.client.ClientSession
    :return: json payload from the Pokemon's API request.
    """
    response = await session.request(method='GET', url=url)

    if response.status == 200:
        json_response = await response.json()
        return json_response

    if response.status == 404:
        return


async def get_requests(all_url: list):
    """
    Method used when the input file argument is provided in the command line.

    :param all_url: string list
    :return: json payload for all Pokemon's API request.
    """
    # This functions takes in a list of urls and makes batch async calls. Returns a list of all responses
    async with aiohttp.ClientSession() as session:
        async_coroutines = [get_single_request(url, session) for url in all_url]
        all_responses = await asyncio.gather(*async_coroutines)
        all_responses_filtered = [response for response in all_responses if response is not None]  # filter out None values
        return all_responses_filtered


def convert_json_into_ability_object(json_list) -> list:
    """
    Take the payload JSON result from API get request calls and use it to create ability objects.

    :param json_list: json list
    :return: List of ability objects
    """
    if len(json_list) == 0:
        return []

    ability_objects = []
    for ability in json_list:
        single_ability = Ability(
            ability['generation']['name'],
            ability['effect_entries'] if ability['effect_entries'] else None,
            ability['pokemon'],
            ability['name'],
            ability['id']
        )
        ability_objects.append(single_ability)

    return ability_objects


def convert_json_into_stat_object(json_list) -> list:
    """
    Take the payload JSON result from API get request calls and use it to create stat objects.

    :param json_list: json list
    :return: List of stat objects
    """
    if len(json_list) == 0:
        return []

    stat_objects = []
    for stat in json_list:
        single_stat = Stat(
            stat['is_battle_only'],
            stat['name'],
            stat['id']
        )
        stat_objects.append(single_stat)

    return stat_objects


def convert_json_into_move_object(json_list) -> list:
    """
    Take the payload JSON result from API get request calls and use it to create move objects.

    :param json_list: json list
    :return: List of move objects
    """
    if len(json_list) == 0:
        return []

    move_objects = []
    for move in json_list:
        single_move = Move(
            move['generation']['name'],
            move['accuracy'],
            move['pp'],
            move['power'],
            move['type']['name'],
            move['damage_class']['name'],
            move['effect_entries'][0]['short_effect'] if move['effect_entries'] and move['effect_entries'][0][
                'short_effect'] else None,
            move['name'],
            move['id']
        )
        move_objects.append(single_move)

    return move_objects


async def get_moves(value_list) -> list:
    """
    Method that is a wrapper to call other functions for move mode.

    :param value_list: string list of input data of pokemon's name or id.
    :return: List of move objects
    """
    moves_url = [f"https://pokeapi.co/api/v2/move/{value}/" for value in value_list]
    moves_api_response = await get_requests(moves_url)
    move_objects = convert_json_into_move_object(moves_api_response)
    return move_objects


async def get_abilities(value_list) -> list:
    """
    Method that is a wrapper to call other functions for ability mode.

    :param value_list: string list of input data of pokemon's name or id.
    :return: List of ability objects
    """
    abilities_url = [f'https://pokeapi.co/api/v2/ability/{value}/' for value in value_list]
    abilities_api_response = await get_requests(abilities_url)
    abilities_objects = convert_json_into_ability_object(abilities_api_response)
    return abilities_objects


async def get_all_pokemon_api_data(value_list):
    """
    Method used to send get API requests for pokemon mode.

    :param value_list: input values for pokemon mode used for multiple get requests
    :return: list of JSON payload data from the api response.
    """
    pokemons_url = [f'https://pokeapi.co/api/v2/pokemon/{value}' for value in value_list]
    pokemons_data_api_response = await get_requests(pokemons_url)
    return pokemons_data_api_response


async def get_pokemon_abilities(data) -> list:
    """
    Method that is a wrapper to call other functions for pokemon mode to extract abilities.

    :param data: string list of input data of pokemon's name or id.
    :return: List of ability objects that is contained in pokemon API result.
    """
    # This function calls get_requests api to get all the json data of abilities, convert to obj Ability, return list of obj Ability

    abilities = data['abilities']
    abilities_url = [ability['ability']['url'] for ability in abilities]
    abilities_api_response = await get_requests(abilities_url)  # all the abilities response from PokeAPI
    ability_objects = convert_json_into_ability_object(abilities_api_response)
    return ability_objects


async def get_pokemon_stats(data) -> list:
    """
    Method that is a wrapper to call other functions for pokemon mode to extract stat.

    :param data: string list of input data of pokemon's name or id.
    :return: List of stat objects that is contained in pokemon API result.
    """
    # This function calls get_requests and then make a list of Stats objects, returns Stats obj list

    stats = data['stats']
    stats_url = [stat['stat']['url'] for stat in stats]
    stats_api_response = await get_requests(stats_url)  # all the stats response from PokeAPI
    stat_objects = convert_json_into_stat_object(stats_api_response)
    return stat_objects


async def get_pokemon_moves(data) -> list:
    """
    Method that is a wrapper to call other functions for pokemon mode to extract moves.

    :param data: string list of input data of pokemon's name or id.
    :return: List of move objects that is contained in pokemon API result.
    """
    # This function calls get_requests and then make a list of Move objects, returns Move obj list

    moves = data['moves']
    moves_url = [move['move']['url'] for move in moves]
    moves_api_response = await get_requests(moves_url)
    move_objects = convert_json_into_move_object(moves_api_response)
    return move_objects


def get_expanded_pokemon(data, moves: list, abilities: list, stats: list) -> Pokemon:
    """
    Method that deals when the expanded argument is mentioned in the command line terminal

    :param data: json payload data return from get pokemon API request
    :param moves: list of move objects
    :param abilities: list of ability objects
    :param stats: list of stats objects
    :return: pokemon object
    """
    ptypes = data['types']
    ptype_name = ", ".join([ptype['type']['name'] for ptype in ptypes])

    single_pokemon = Pokemon(
        data['height'],
        data['weight'],
        stats,
        ptype_name,
        abilities,
        moves,
        data['name'],
        data['id']
    )

    return single_pokemon


async def get_non_expanded_pokemon(data) -> Pokemon:
    """
    Method that deals when the expanded argument is not mentioned in the command line terminal

    :param data: json payload data return from get pokemon API request
    :return: pokemon object
    """
    stats = data['stats']
    stats_info = [(stat['stat']['name']).title() + ': ' + str(stat['base_stat']) for stat in stats]

    abilities = data['abilities']
    abilities_info = ['Name: ' + ability['ability']['name'] for ability in abilities]

    ptypes = data['types']
    ptype_name = ", ".join([ptype['type']['name'] for ptype in ptypes])

    moves = data['moves']
    moves_info = ["Move name: " + move["move"]["name"] + " | Level acquired: " + str(move["version_group_details"][0]["level_learned_at"]) for move in moves]

    single_pokemon = Pokemon(
        data['height'],
        data['weight'],
        stats_info,
        ptype_name,
        abilities_info,
        moves_info,
        data['name'],
        data['id']
    )

    return single_pokemon
