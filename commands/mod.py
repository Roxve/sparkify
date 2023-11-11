from setup import *


@bot.slash_command("say", "make the bot say something (you can add role buttons/link buttons to bot messages)",default_member_permissions=discord.Permissions(administrator=True))
async def say(interaction: discord.Interaction, msg: str):
    await interaction.response.send_message("success", ephemeral=True)
    await interaction.channel.send(msg)

class RoleButton(discord.ui.Button):
    role_id = 0
    def __init__(self,label, style, role_id: int): 
       super().__init__(
                        custom_id=f"{role_id}",
                        label=label,
                        style=style
                       )
       self.role_id = role_id
    
    #@classmethod
    async def callback(self,interaction:discord.Interaction):
        print(self.role_id)
        role_id = self.role_id
        print(role_id)
        role = interaction.guild.get_role(role_id)
        if role in interaction.user.roles:
            try: 
                await interaction.user.remove_roles(role)
            except:
                await interactuon.response.send_message(f"faild removing role, notify the server admin!",  ephemeral=True)
            else:
                await interaction.response.send_message(f"Removed role {role.name}!", ephemeral=True)
        else:
            try:
                await interaction.user.add_roles(role)
            except:
                await interaction.response.send_message(f"faild removing role, notify the server admin!",  ephemeral=True)
            else:
                await interaction.response.send_message(f"Added role {role.name}!", ephemeral=True)

class ButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        #self.buttons = buttons
        #for label , role in buttons.items():
            #self.add_item(RoleButton(label, discord.ButtonStyle.primary, role.id))


@bot.slash_command("adds a role button to a bot message",default_member_permissions=discord.Permissions(administrator=True))
async def add_role_button(interaction: discord.Interaction,label: str, role: discord.Role,message_link: str):
    guild = interaction.guild.id
    message_link = message_link.replace(f"https://discord.com/channels/{guild}/", "")
    ids = message_link.split('/') 
    ids = [int(ids[0]), int(ids[1])]
    
    channel: discord.Channel = bot.get_channel(ids[0])
    message = await channel.fetch_message(ids[1])
    message_view = discord.ui.View.from_message(message) 
    
    view = None
    if message_view is None:
        view = ButtonsView()
    else:
        view = message_view
    view.add_item(RoleButton(label, discord.ButtonStyle.primary, role.id))
    
    try:
        await message.edit(message.content, view=view)
    except:
        await interaction.response.send_message("roles buttons cannot be duplicate!", ephemeral=True)    
        return
    await interaction.response.send_message("success", ephemeral=True)
    
