"""Module contains our facade, request, and commandline setup"""

# Name: April Cheng
# Student number: A01261858
# Name: Benjamin Chen
# Student number: A01268070

import argparse
import asyncio
import datetime
from datetime import datetime
from pokeretriever.helper_functions import get_pokemon_stats, get_pokemon_moves, get_pokemon_abilities, \
    get_expanded_pokemon, read_file, get_moves, get_abilities, get_all_pokemon_api_data, get_non_expanded_pokemon


class Request:
    """
    Class is used to represent from command line to get Pokemon data from an API.
    """

    def __init__(self):
        """
        Initialize the data attributes of a request object.
        """
        self.mode = None
        self.input_file = None
        self.input_data = None
        self.expanded = None
        self.output = None

    def __str__(self):
        """
        Method used to return the command line arguments specified in terminal.

        :return: String of formatted command line arguments.
        """
        return (f"Mode: {self.mode}\n"
                f"InputFile: {self.input_file}\n"
                f"InputData: {self.input_data}\n"
                f"Expanded: {self.expanded}\n"
                f"Output: {self.output}\n")


class Facade:
    """
    Class used to handle request from either console or input file and output the results to console or a file.
    """

    @staticmethod
    async def execute_request(request: Request):
        """
        Method that depends on the command line argument given by the user and will perform various tasks to
        grab either 'move', 'ability', 'pokemon' using a batch query (input file) or single query (input data).
        Output result in a file or to console.

        :param request: string value specified by the user to request information based on either 'move', 'ability',
                        and 'pokemon'
        :return: None
        """
        # ------------------------- Handling mode move ------------------------- #
        if request.mode == 'move':
            if request.input_file:
                move_values_from_file_list = read_file(request.input_file)  # gets all the values from file
                move_objects = await get_moves(move_values_from_file_list)  # returns move objects
            else:
                #  if no file input, just input value is entered in the terminal
                input_data = request.input_data
                move_objects = await get_moves([input_data])  # should just return one move object

            print_or_output_file(move_objects, request)

        # ------------------------- Handling mode ability ------------------------- #
        if request.mode == 'ability':
            if request.input_file:
                ability_values_from_file_list = read_file(request.input_file)  # gets all the values from file
                ability_objects = await get_abilities(ability_values_from_file_list)  # returns ability objects
            else:
                input_data = request.input_data
                ability_objects = await get_abilities([input_data])  # should just return one ability object

            print_or_output_file(ability_objects, request)

        # ------------------------- Handling mode pokemon ------------------------- #
        if request.mode == 'pokemon':
            if request.input_file:
                # if there is file input, grab data from api for all pokemon in the file
                pokemon_values_from_file_list = read_file(request.input_file)
                data_list = await get_all_pokemon_api_data(
                    pokemon_values_from_file_list)  # return api response for all pokemon
            else:
                input_data = request.input_data
                data_list = await get_all_pokemon_api_data([input_data])  # return one api response for one pokemon

            pokemon_list = []
            for data in data_list:
                if request.expanded:
                    move_objects = await get_pokemon_moves(data)
                    ability_objects = await get_pokemon_abilities(data)
                    stat_objects = await get_pokemon_stats(data)
                    single_pokemon = get_expanded_pokemon(data, move_objects, ability_objects, stat_objects)
                else:
                    single_pokemon = await get_non_expanded_pokemon(data)

                pokemon_list.append(single_pokemon)

            print_or_output_file(pokemon_list, request)


def setup_request_commandline():
    """
    Implements the argparse module to accept arguments via the command
    line. This function specifies what these arguments are and parses it
    into an object of type Request. If something goes wrong with
    provided arguments then the function prints an error message and
    exits the application.

    :return: The object of type Request with all the arguments provided
    in it.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("mode", choices=['pokemon', 'ability', 'move'], help="Pokemon will query for general pokemon "
                                                                             "information. Ability will query for "
                                                                             "pokemon ability information. Move "
                                                                             "will query for pokemon movement "
                                                                             "information.")

    group_input = parser.add_mutually_exclusive_group(required=True)
    group_input.add_argument("--inputfile", help="User provides a file that contains multiple query to run at a batch")
    group_input.add_argument("--inputdata", help="User need to provide a pokemon name or ID for running a single query")

    parser.add_argument("--expanded", action="store_true", help="Optional flag, when specified, certain attributes will"
                                                                "be expanded as sub-queries of certain attributes will "
                                                                "trigger.")

    parser.add_argument("--output", help="Optional flag, if specified, a filename with .txt extension must also be "
                                         "provided the query result should be printed to the specified text file")

    try:
        args = parser.parse_args()
        request = Request()
        request.mode = args.mode
        if args.inputdata is None:
            request.input_file = args.inputfile
        else:
            request.input_data = args.inputdata
        request.expanded = args.expanded
        request.output = args.output
        return request
    except Exception as e:
        print(f"Error! Could not read arguments.\n{e}")
        quit()


def print_or_output_file(obj_list, request: Request):
    """
    Method to determine whether to output the result to console or to a file.

    :param obj_list: Pokemon data object, 'move', 'ability', 'pokemon'
    :param request: Request Type object
    :return: None.
    """
    today_date = datetime.now()
    timestamp = today_date.strftime("%d/%m/%Y %H:%M")

    # if writing to file
    if request.output:
        path = request.output
        with open(path, 'w') as file:
            if len(obj_list) == 0:
                file.write(f'Query is invalid.')
            else:
                file.write(f'Timestamp: {timestamp}\nNumber of requests: {len(obj_list)}\n')
                for obj in obj_list:
                    file.write(f'{str(obj)}\n\n')

        print(f'Finish processing. See output file {request.output}')

    else:
        # if printing to console
        if len(obj_list) == 0:
            print(f'Query is invalid')
        else:
            print(f'Timestamp: {timestamp}\nNumber of requests: {len(obj_list)}\n')
            for obj in obj_list:
                print(f'{obj}\n\n')


async def main():
    """
    Used to run our Pokemon API. Uses a Facade pattern.

    :return: none.
    """
    request = setup_request_commandline()
    facade = Facade()
    await facade.execute_request(request)


if __name__ == '__main__':
    asyncio.run(main())
