from setup import *


@bot.slash_command("say", "make the bot say something (you can add role buttons/link buttons to bot messages)",default_member_permissions=nextcord.Permissions(administrator=True))
async def say(interaction: nextcord.Interaction, msg: str):
    await interaction.response.send_message("success", ephemeral=True)
    await interaction.channel.send(msg)

class RoleButton(nextcord.ui.Button):
    role_id = 0
    def __init__(self,label, style, role_id: int): 
       super().__init__(
                        custom_id=f"{role_id}",
                        label=label,
                        style=style
                       )
       self.role_id = role_id
    
    #@classmethod
    async def callback(self,interaction:nextcord.Interaction):
        print(self.role_id)
        role_id = self.role_id
        print(role_id)
        role = interaction.guild.get_role(role_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Removed role {role.name}!", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Added role {role.name}!", ephemeral=True)

class RoleButtonsView(nextcord.ui.View):
    def __init__(self, buttons):
        super().__init__(timeout=None)
        self.buttons = buttons
        for label , role in buttons.items():
            self.add_item(RoleButton(label, nextcord.ButtonStyle.primary, role.id))


@bot.slash_command("add-button", "adds a button to a bot message",default_member_permissions=nextcord.Permissions(administrator=True))
async def add_button(interaction: nextcord.Interaction,label: str, role: nextcord.Role,message_link: str):
    guild = interaction.guild.id
    message_link = message_link.replace(f"https://discord.com/channels/{guild}/", "")
    ids = message_link.split('/') 
    ids = [int(ids[0]), int(ids[1])]
    
    channel: nextcord.Channel = bot.get_channel(ids[0])
    message = await channel.fetch_message(ids[1])

    view = RoleButtonsView({label: role})
    
    await message.edit("test fr", view=view)
    
    await interaction.response.send_message("success", ephemeral=True)
    
