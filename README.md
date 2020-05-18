# Discord Indexing Bot

## Introduction
+ This is a tool bot that help you build an index file of your guild.

## Requirements
+ Python 3.6+
+ pipenv
+ discord.py

## Usage
+ Build the environment using `pipenv`.
+ Rename `.env.template` into `.env` and put your token of bot after `TOKEN=`.
+ (Optional) Rename `config.json.template` into `config.json` and fill in.
  + `title` is the meta of title.
  + `desc` is the meta of description.
  + `header` is the header of markdown file.
  + `ignored_channels` is a list of channel that you want to ignore.
+ Run bot by `pipenv run python main.py`.
+ The result file will be named `{Guild Name}.md`.

## Contact Information
+ If you have any problem, welcome to open a issue.
+ You can contact me in discord `PenutChen#2135` if you like.

## License
+ Licensed under the MIT license.
