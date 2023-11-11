import discord
from setup import *
from commands.etc import *
from commands.economy import *
from commands.mod import *

@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')
    
    print("setup hook")
    bot.add_view(ButtonsView())
    # bot.add_dynamic_items(RoleButton)
@bot.event
async def on_message(msg):
    if msg.author.bot:
        return
    if "spark" in msg.content.lower():
        await msg.reply('🔥')
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.is_component():
        id: str = interaction.custom_id
        print(id)
        if id.startswith("role_"):
            role_id = int(id.replace("role_", ""))
            role = interaction.guild.get_role(role_id)
            if role in interaction.user.roles:
                try: 
                    await interaction.user.remove_roles(role)
                except:
                    await interaction.response.send_message(f"faild removing role, notify the server admin!",  ephemeral=True)
                else:
                    await interaction.response.send_message(f"🛑 removed role @{role.name} from your roles!", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                except:
                    await interaction.response.send_message(f"faild removing role, notify the server admin!",  ephemeral=True)
                else:
                    await interaction.response.send_message(f"🎉 added role @{role.name} to your roles!", ephemeral=True)     
        else:
            await bot.process_application_commands(interaction)
    else:
        await bot.process_application_commands(interaction)
 

bot.run(token)
print("Exit 0")
