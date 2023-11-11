
import discord
from discord.ext import commands
import pickledb
import os
import random
import datetime
# bot setup
token = os.environ.get('token')
intents = discord.Intents.default()

intents.members = True
intents.message_content = True

bot = discord.Bot(intents=intents)

# data setup
data = pickledb.load("data.db", True)

async def reply(ctx , content="", embeds=[]):
    command_name = ctx.command.name
    embed = discord.Embed(
        #title=command_name,
        description=content,
        colour=discord.Color.blue()
    )
    embed.set_author(name=f'/{command_name}', icon_url=ctx.user.avatar)
    embed.set_footer(text=f'executed by {ctx.user.name}')
    
    await ctx.respond(embed=embed)


async def set_data(guild_id,obj_id, obj_prop, value):
    return data.set(f'{guild_id}_{obj_id}_{obj_prop}', value)

async def get_data(guild_id,obj_id, obj_prop):
    return data.get(f'{guild_id}_{obj_id}_{obj_prop}')

async def setup_usr(guild_id,user_id): 
    if not await get_data(guild_id, user_id, 'money'):
        await set_data(guild_id,user_id, 'money', 0)
    if not await get_data(guild_id, user_id, 'shifts'):
        await set_data(guild_id,user_id, 'shifts', 0)  
    if not await get_data(guild_id, user_id, 'job'):
        await set_data(guild_id,user_id, 'job', {"job": "none", "min": 0, "max": 0})   
    # add more user data here

async def isSetup(guild_id, user_id):
    await setup_usr(guild_id ,user_id);

async def SetupGuild(guild_id):
    if not await get_data(guild_id, '','jobs'):
        await set_data(guild_id, '', 'jobs',
        {
            "developer": {"min": 150, "max": 600, "shifts": 80}, 
            "sparkify developer": {"min": 500,"max": 850, "shifts": 120}, 
            "janitor": {"min": 50, "max": 200, "shifts": 0},
            "driver": {"min": 100, "max": 400, "shifts": 40}
        })

async def timeoutUsage(guild_id, user_id, command, ms):
    await set_data(guild_id, user_id, f'{command}_timeout', (datetime.datetime.now().timestamp() * 1000) + ms)


async def isTimeouted(guild_id, user_id, command):
    timeout = await get_data(guild_id, user_id, f'{command}_timeout')   
    if timeout is False:
        return False
    return timeout > (datetime.datetime.now().timestamp() * 1000)
 
