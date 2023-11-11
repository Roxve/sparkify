from setup import *


@bot.slash_command(name="say", description="make the bot say something (you can add role buttons/link buttons to bot messages)",default_member_permissions=discord.Permissions(administrator=True))
async def say(ctx , msg: str):
    await ctx.respond("success", ephemeral=True)
    await ctx.channel.send(msg)

@bot.slash_command(name="edit", description="edits a bot message",default_member_permissions=discord.Permissions(administrator=True))
async def edit(ctx , content: str, message_link: str):
    guild = ctx.guild.id
    message_link = message_link.replace(f"https://discord.com/channels/{guild}/", "")
    ids = message_link.split('/') 
    ids = [int(ids[0]), int(ids[1])]
    
    channel: discord.Channel = bot.get_channel(ids[0])
    message = await channel.fetch_message(ids[1])
    await message.edit(content=content)
    await ctx.respond("success", ephemeral=True)


class RoleButton(discord.ui.Button):
    role_id = 0
    def __init__(self,label, style, role_id: int): 
       super().__init__(
                        custom_id=f"role_{role_id}",
                        label=label,
                        style=style
                       )
       self.role_id = role_id
    
    #@classmethod
    """async def callback(self,ctx):
        print(self.role_id)
        role_id = self.role_id
        print(role_id)
        role = ctx.guild.get_role(role_id)
        if role in ctx.user.roles:
            try: 
                await ctx.user.remove_roles(role)
            except:
                await ctx.response.send_message(f"faild removing role, notify the server admin!",  ephemeral=True)
            else:
                await ctx.response.send_message(f"Removed role {role.name}!", ephemeral=True)
        else:
            try:
                await ctx.user.add_roles(role)
            except:
                await ctx.response.send_message(f"faild removing role, notify the server admin!",  ephemeral=True)
            else:
                await ctx.response.send_message(f"Added role {role.name}!", ephemeral=True)"""

class ButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        #self.buttons = buttons
        #for label , role in buttons.items():
            #self.add_item(RoleButton(label, discord.ButtonStyle.primary, role.id))


@bot.slash_command(name="add-role-button",description="adds a role button to a bot message",default_member_permissions=discord.Permissions(administrator=True))
async def add_role_button(ctx ,label: str, role: discord.Role,message_link: str):
    guild = ctx.guild.id
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
        await ctx.respond("roles buttons cannot be duplicate or message is non bot message!", ephemeral=True)    
        return
    await ctx.respond("success", ephemeral=True)
    
@bot.slash_command(name="remove-button",description="removes a button from a bot message",default_member_permissions=discord.Permissions(administrator=True))
async def remove_button(ctx ,button: int,message_link: str):
    guild = ctx.guild.id
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
    if view.children.__len__() < button:
        await ctx.respond(f"there is only {view.children.__len__()} buttons in message!")
        return
    view.remove_item(view.children[button - 1])
    
    await message.edit(message.content, view=view)
    await ctx.respond("success", ephemeral=True)
 
