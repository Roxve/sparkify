from setup import *
import random

# enconmy
@bot.slash_command(name="balance", description="displays user balance")
async def balance(ctx, user: discord.User = None):
    if user is None:
        user = ctx.user
    embed = discord.Embed(
        #title=f'{user.name}',
        color=discord.Color.blue()
    )
    await isSetup(ctx.guild.id ,user.id)
    embed.set_author(name=user.name, icon_url=user.avatar)
    money = await get_data(ctx.guild.id ,user.id, "money")
    embed.add_field(name='Money:', value=f'🪙 {money}')
    await ctx.respond(embed=embed)

@bot.slash_command(name="set-money", description="sets user money",default_member_permissions=discord.Permissions(administrator=True))
async def set_money(ctx, money: int, user: discord.User = None):
    if user is None:
        user = ctx.user
    money = abs(money)
    
    await isSetup(ctx.guild.id, user.id)
    await set_data(ctx.guild.id ,user.id, 'money',money)
    await reply(ctx, content=f'successfully set {user} money to {money}')


@bot.slash_command(name="rob", description="robs a users money")
async def rob(ctx, user: discord.User):
    robber = ctx.user    
    guild_id = ctx.guild.id
    
    if await isTimeouted(guild_id, robber.id, "rob"):
        await reply(ctx, content=f'you have to wait for 5 hours to attempt robbing another person!')
        return
        
    random_num = random.randint(0,99)
    robber_money = await get_data(guild_id, robber.id, 'money')
    user_money = await get_data(guild_id, user.id, 'money')    
    
    if random_num < 42:
        await timeoutUsage(guild_id, robber.id, "rob", 18000000)
        money = random.randint(1, round(user_money / 3.5))

        await set_data(guild_id, user.id, 'money', user_money - money)
        await set_data(guild_id, robber.id, 'money', robber_money + money)
        
        await reply(ctx, content=f'{robber} robbed {money} from {user}')
    else:

        money = random.randint(1, round(robber_money / 4))
        
        await set_data(guild_id, robber.id, 'money', robber_money - money)        
        
        await timeoutUsage(guild_id, robber.id, "rob", 18000000)
        await reply(ctx, content=f'{robber} faild robbing {user}, you have been fined {money}')

    
@bot.slash_command(name="give-money", description="gives user an ammount of money")
async def give_money(ctx, money: int, user: discord.User):
    money = abs(money) # makes money positive to avoid errors
    guild_id = ctx.guild.id
    giver = ctx.user
    
    await isSetup(guild_id, user.id)
    await isSetup(guild_id, giver.id)

    giver_money = await get_data(guild_id, giver.id, 'money')
    user_money = await get_data(guild_id, user.id, 'money')

    if giver_money < money:
        await reply(ctx, content='error you dont have enough money!')
        return
    
    
    await set_data(guild_id ,user.id, 'money', user_money + money)
    await set_data(guild_id ,giver.id, 'money', giver_money - money)

    await reply(ctx, content=f'successfully give {money} of money to {user}')



@bot.slash_command(name="list-jobs", description="lists server jobs")
async def list_jobs(ctx):
    guild = ctx.guild.id
    await SetupGuild(guild)
    jobs = await get_data(guild, '', 'jobs')
    results = "jobs in this server:\n"
    for key, val in jobs.items():
        results += f"**{key}**: min {val['min']}, max {val['max']}, shifts required {val['shifts']}\n"
    await reply(ctx, content=results)

@bot.slash_command(name="choose-job", description="choose your job")
async def choose_job(ctx, job: str):
    guild = ctx.guild.id
    user = ctx.user
    await setup_usr(guild, user.id)
    await SetupGuild(guild)
    jobs = await get_data(guild, '', 'jobs')

    shifts = await get_data(guild, user.id, 'shifts')

    job = job.lower()
    
    for key, val in jobs.items():
        if key == job:
            if val["shifts"] > shifts:
                await reply(ctx, content=f"not enough shifts! {key} requires {val['shifts']} shifts you have {shifts}!")
                return 
            await set_data(guild, user.id, 'job', {"job": key, "min": val["min"], "max": val["max"]})
            await reply(ctx, content="succesfully set your job!")
            return
    await reply(ctx, content=f"error unknown job! {job}")


@bot.slash_command(name="work", description="work your job!")
async def work(ctx):
    user = ctx.user
    guild = ctx.guild.id
    if await isTimeouted(guild, user.id, 'work'):
        await reply(ctx, content="you have to wait one hour before working!")
        return

    await setup_usr(guild, user.id)
    job = await get_data(guild, user.id, 'job')
    if job["job"] == "none":
        await reply(ctx, content="you dont have a job! list jobs by /list-jobs, choose one by /choose-job")
        return

    money = await get_data(guild, user.id, 'money')
    moneyEarn = random.randint(job["min"], job["max"])
    shifts = await get_data(guild, user.id, 'shifts')
    
    await set_data(guild, user.id, 'money',money + moneyEarn);
    await set_data(guild, user.id, 'shifts', shifts + 1)
    await timeoutUsage(guild, user.id, 'work', 3600000)
    await reply(ctx, content=f"you worked as {job['job']}, and earned {moneyEarn}")
    
