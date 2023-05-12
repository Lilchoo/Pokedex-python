# An Object-oriented Pokedex

## Summary
This assignment is getting exposure to implementing and writing code using asynchronous features such as asyncio and aiohttp packages to make GET HTTP request.
The objective of this task is create our own prototype of Professor Oaks Pokedex by using the PokeAPI.

### How it works:

In this program, users will be using the command line terminal to input data in two ways and get a result that can be outputted in two ways as well.

Below is the following syntax to run the program.
`python pokedex.py {"pokemon" | "ability" | "move"} {--inputfile 
"filename.txt" | --inputdata "name or id"} [--expanded] [--output "<NAME>.txt"]`

This program currently supports three modes {"pokemon" | "ability" | "move"} which the user needs to choose one of them.
- <b>pokemon mode</b>: The input will be an id or the name of a pokemon. The pokedex will query pokemon information
- <b>ability mode</b>: The input will be an id or the name of a ability. These are certain effects that
pokemon can enable. The pokedex will query the ability information
- <b>move mode</b>, the input will be an id or the name of a pokemon move. These are the
attacks and actions pokemon can take. The pokedex will query the move information.

Next the user can either select two options to input data {--inputfile "filename.txt" | --inputdata "name or id"} which the user will need to choose one of them.
- <b>inputdata</b>: Will only suuport one query at a time. Value is dependent on the mode
- <b>inputfile</b>: Will support one or more queries. Again value is dependent on the mode

Next option [--expanded] is used only for the pokemon mode. It will expand certain attribtues by doing subquries for additional information.
- By simply including '--expanded' will trigger more detail. If the user want brief information, do not include this option.

Last option [--output "<NAME>.txt"] is used to output the results to a file. If this argument is not provided, the result will be shown to the consolve instead.