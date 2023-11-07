import nextcord
from nextcord.ext import commands
import pickledb
import os

# bot setup
token = os.environ.get('token')
intents = nextcord.Intents.default()

intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents)

# data setup
data = pickledb.load("data.db", True)

async def reply(interaction: nextcord.Interaction, content="", embeds=[]):
    command_name = interaction.data['name']
    embed = nextcord.Embed(
        #title=command_name,
        description=content,
        colour=nextcord.Color.blue()
    )
    embed.set_author(name=f'/{command_name}', icon_url=interaction.user.avatar)
    embed.set_footer(text=f'executed by {interaction.user.name}')
    
    await interaction.response.send_message(embed=embed)


async def set_data(guild_id,obj_id, obj_prop, value):
    return data.set(f'{guild_id}_{obj_id}_{obj_prop}', value)

async def get_data(guild_id,obj_id, obj_prop):
    return data.get(f'{guild_id}_{obj_id}_{obj_prop}')

async def setup_usr(guild_id,user_id):
    await set_data(guild_id,user_id, '', True)
    await set_data(guild_id,user_id, 'money', 0)
    # add more user data here

async def isSetup(guild_id, user_id):
    if await get_data(guild_id ,user_id, '') == False:
        await setup_usr(guild_id ,user_id);
        return False;
    else:
        return True;

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')


@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    if "spark" in msg.content.lower():
        await msg.reply('🔥')

@bot.slash_command("help", "displays commands")
async def help(interaction: nextcord.Interaction):
    await reply(interaction, content=
    """
    - etc: 
        - /help -> displays this help
- enconomy:
    - /balance -> displays user balance"""
)


# enconmy
@bot.slash_command("balance", "displays user balance")
async def balance(interaction: nextcord.Interaction, user: nextcord.User = None):
    if user is None:
        user = interaction.user
    embed = nextcord.Embed(
        #title=f'{user.name}',
        color=nextcord.Color.blue()
    )
    await isSetup(interaction.guild.id ,user.id)
    embed.set_author(name=user.name, icon_url=user.avatar)
    money = await get_data(interaction.guild.id ,user.id, "money")
    embed.add_field(name='Money:', value=f'🪙 {money}')
    await interaction.response.send_message(embed=embed)

@bot.slash_command("set-money", "sets user money",default_member_permissions=nextcord.Permissions(administrator=True))
async def set_money(interaction: nextcord.Interaction, money: int, user: nextcord.User = None):
    if user is None:
        user = interaction.user
    money = abs(money)
    
    await isSetup(interaction.guild.id, user.id)
    await set_data(interaction.guild.id ,user.id, 'money',money)
    await reply(interaction, content=f'successfully set {user} money to {money}')



@bot.slash_command("give-money", "sets user money")
async def set_money(interaction: nextcord.Interaction, money: int, user: nextcord.User):
    money = abs(money) # makes money positive to avoid errors
    guild_id = interaction.guild.id
    giver = interaction.user
    
    await isSetup(guild_id, user.id)
    await isSetup(guild_id, giver.id)

    giver_money = await get_data(guild_id, giver.id, 'money')
    user_money = await get_data(guild_id, user.id, 'money')

    if giver_money < money:
        await reply(interaction, content='error you dont have enough money!')
        return
    
    
    await set_data(guild_id ,user.id, 'money', user_money + money)
    await set_data(guild_id ,giver.id, 'money', giver_money - money)

    await reply(interaction, content=f'successfully give {money} of money to {user}')

bot.run(token)
print("Exit 0")
