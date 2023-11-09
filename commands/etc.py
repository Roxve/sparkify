from setup import *


@bot.slash_command("help", "displays commands")
async def help(interaction: nextcord.Interaction):
    await reply(interaction, content=
    """
    - etc: 
        - /help -> displays this help
- enconomy:
    - /balance -> displays user balance
    - /set-money -> sets user money (admin)
    - /give-money -> gives a user money from balance
    - /rob -> robs a person"""
)
