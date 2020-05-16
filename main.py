import json
import os
import re
import sys

import discord

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} | Ready!')
    for guild in client.guilds:
        print(f'{client.user} | Building index for {guild.name}')
        index = {}
        category_ids = {}
        category = {}
        for channel in guild.channels:
            if isinstance(channel, discord.CategoryChannel):
                category_ids[channel.id] = channel.name.title()
            if isinstance(channel, discord.TextChannel):
                channels = category.get(channel.category_id, list())
                channels.append(channel.name)
                category[channel.category_id] = channels
                index[channel.name] = []
                async for msg in channel.history():
                    if 'https' in msg.content:
                        asset = {
                            'Author': str(msg.author),
                            'Date': msg.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'Content': msg.clean_content
                        }
                        for embed in msg.embeds:
                            if embed.title != discord.Embed.Empty:
                                asset['Embed'] = embed.title
                        index[channel.name].append(asset)
        category = {
            'category_ids': category_ids,
            'category': category
        }
        idx2md(index, category, guild.id, f'./{guild.name}.md')

    print(f'{client.user} | Done!')
    await client.logout()
    await client.close()

@client.event
async def on_message(message: discord.Message):
    if message.content == '!b':
        print(f'{client.user} | Close!')
        await client.logout()
        await client.close()


def match_url(t):
    m = re.search(r'https?:\/\/[\w@:%._\+~#=\/\-]+', t, re.M)
    if m:
        return m.group(0)
    return None

def idx2md(index, category, guild_id, out=sys.stdout):
    guild_id = str(guild_id)
    if os.path.exists('./config.json'):
        with open('./config.json', 'r', encoding='UTF-8') as f:
            config = json.load(f).get(guild_id, None)

    if isinstance(out, str):
        out = open(out, 'w', encoding='UTF-8')

    def print_fn(*args, **kwargs):
        print(*args, **kwargs, file=out)

    if config:
        title = config.get('title', '')
        desc = config.get('desc', '')
        header = config.get('header', '')
        print_fn(
            '---\n'
            f'title: \'{title}\'\n'
            f'description: \'{desc}\'\n'
            '---\n\n'
            f'# {header}\n\n[TOC]\n'
        )

    for ignored in config.get('ignored_channels', list()):
        index[ignored] = []

    category_ids = category['category_ids']

    for category_id in category['category']:
        print_fn(f'## {category_ids[category_id]}')
        categories = category['category'][category_id]
        for channel_name in categories:
            if index[channel_name]:
                print_fn(f'### {channel_name.title()}')
            for msg in index[channel_name]:
                author = msg['Author']
                date = msg['Date']
                content = msg['Content'].replace('```', '')
                content = content.split('\n')
                content = '\n  '.join(content)
                url = match_url(content)
                embed_title = msg.get('Embed', None)

                print_fn(f'+ Author: {author}')
                print_fn(f'+ Date: {date}')
                if embed_title is not None:
                    print_fn(f'+ Title: {embed_title}')
                if url is not None:
                    print_fn(f'+ Url: {url}')
                print_fn(f'+ Content:')
                print_fn(f'  ```\n  {content}\n  ```')
                print_fn('\n---\n')

    if out != sys.stdout:
        out.close()

if __name__ == '__main__':
    token = os.environ['TOKEN']
    client.run(token)
