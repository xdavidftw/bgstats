import discord
import asyncio
import requests
import os

BOT_TOKEN = os.environ['BOT_TOKEN']
FORTNITE_API_TOKEN = os.environ['FORTNITE_API_TOKEN']
COMMAND_PREFIX = '!'

client = discord.Client()

@client.event
async def on_ready():
  await client.change_presence(game=discord.Game(name='Напиши !help'))

@client.event
async def on_message(message):
  if message.content.startswith(COMMAND_PREFIX + 'help'):
    await client.send_message(message.channel, 'Бота е направен със Fortnite Traker API и ще може да ви казва само Lifestats . Напиши `' + COMMAND_PREFIX + 
      'stats <platform> <nickname>` и ще получиш Lifestats.')
  elif message.content.startswith(COMMAND_PREFIX + 'ping'):
    await client.send_message(message.channel, 'pong')

  if message.content.startswith(COMMAND_PREFIX + 'stats'):
    words = message.content.split(' ', 2)

    if len(words) < 3:
      await client.send_message(message.channel, 'Употреба: ' + COMMAND_PREFIX + 'stats <pc,xbl,psn> <nickname>')
      return

    platform = words[1].lower()

    # more acceptable platform names
    if platform == 'xbox':
      platform = 'xbl'
    elif platform == 'ps4':
      platform = 'psn'

    if platform not in ('pc','xbl','psn'):
      await client.send_message(message.channel, 'Употреба: ' + COMMAND_PREFIX + 'stats <pc,xbl,psn> <nickname>')
      return
    else:
      res = fortnite_tracker_api(platform,words[2])

      if res:
        matches_played = res[0]['value']
        wins = res[1]['value']
        win_percent = res[2]['value']
        kills = res[3]['value']
        kd = res[4]['value']

        embed = discord.Embed(title="Lifetime Stats за " + words[2], color=D48D22)

        embed.add_field(name="Изиграни Мачове", value=matches_played + '\n', inline=False)
        embed.add_field(name="Победи", value=wins + '\n', inline=False)
        embed.add_field(name="Win %", value=win_percent + '\n', inline=False)
        embed.add_field(name="Убийства", value=kills + '\n', inline=False)
        embed.add_field(name="K/D", value=kd + '\n', inline=False)
        await client.send_message(message.channel, embed=embed)
      else:
        await client.send_message(message.channel, 'Данните не можаха да бъдат получени. Проверете двукратно изписването на псевдонима си.')

def fortnite_tracker_api(platform, nickname):
  URL = 'https://api.fortnitetracker.com/v1/profile/' + platform + '/' + nickname
  req = requests.get(URL, headers={"TRN-Api-Key": FORTNITE_API_TOKEN})

  if req.status_code == 200:
    try:
      print(req.json())
      lifetime_stats = req.json()['lifeTimeStats']
      return lifetime_stats[7:]
    except KeyError:
      return False
  else:
    return False

client.run(BOT_TOKEN)
