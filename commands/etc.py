from setup import *


@bot.slash_command()
async def help(ctx):
    await reply(ctx, content=
    """
    - etc: 
        - /help -> displays this help
- enconomy:
    - /balance -> displays user balance
    - /set-money -> sets user money (admin)
    - /give-money -> gives a user money from balance
    - /rob -> robs a person"""
)
