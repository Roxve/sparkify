import nextcord
from setup import *
from commands.etc import *
from commands.economy import *
from commands.mod import *

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')


@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    if "spark" in msg.content.lower():
        await msg.reply('🔥')


bot.run(token)
print("Exit 0")
