from discord.ext import commands

from main import login, registerUser, checkIn, unregister
from settings import DISCORD_TOKEN

bot = commands.Bot(command_prefix='.', help_command=None)

@bot.command()
async def help(ctx):
    await ctx.send("""
```
.userdetails email:password:username (Can only be used in DMs with the bot, register user details to the bot)
For example: .userdetails deviance@gmail.com:qwerty123:deviance69

.register [challongelink] (Registers the user to this event)
For example: .register https://challonge.com/7way2nqm

.checkin [challongelink] (Checks-in the user for this event)
For example: .checkin https://challonge.com/7way2nqm

.unregister [challongelink] (Unregisters the user for this event)
For example: .unregister https://challonge.com/7way2nqm

.github (Contains the source code for the bot)
For example: .github

.clearDM (Can only be used in DMs with the bot, clear the last 100 bot messages)
For example: .clearDM
```
    """)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, commands.PrivateMessageOnly):
        await ctx.send("Command can only be used in DMs")

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command(name='test')
@commands.is_owner()
async def test(ctx):
    await ctx.send("Bot is being tested! \nMessage will delete in 5 secs", delete_after=5)
    print(format(ctx.message.author))

@bot.command(name='clearDM')
@commands.dm_only()
async def clearDM(ctx):
    print("Purging...")

    channel = ctx.channel
    async for message in channel.history(limit=100):
        if message.author == bot.user:
            await message.delete()

    print("Purge complete!")
    await ctx.send("Purged! \nMessage will delete in 5 secs", delete_after=5)

@bot.command(name='github')
async def github(ctx):
    await ctx.send("https://github.com/Devianc3WasTaken/ChallongeBot/")

@bot.command(name='shutdown')
@commands.is_owner()
async def shutdown(ctx):
    print("Bot has been shutdown!")
    await ctx.bot.close()

@bot.command(name='userdetails')
@commands.dm_only()
async def userDetails(ctx):
    await ctx.send("Success, if your user information is incorrect please edit the message to the correct information or use the command again!")

async def checkUserDetails(ctx):
    #print("Checking if user has given login information...")
    channel = ctx.author
    messages = await channel.history(oldest_first=False).flatten()

    #print("Looping messages...")
    for msg in messages:
        if ".userdetails" in msg.content:
            userInfo = msg.content.replace(".userdetails ", "")
            userInfo = userInfo.split(":")
            #print("information found!")
            return True, userInfo

    #print("Information not found!")
    return False, None

@bot.command(name='register', pass_context=True)
async def register(ctx, challongeLink):
    hasDetails, loginDetails = await checkUserDetails(ctx)
    if not hasDetails:
        await ctx.send('Please DM me your login details using ".userdetails email:password:username"! \nMessage will delete in 10 secs', delete_after=10)
        return

    session, authToken = login(loginDetails[0], loginDetails[1], False)
    tournamentRules = registerUser(session, loginDetails[2], authToken, challongeLink, True)

    print(format(ctx.message.author))
    userID = ctx.message.author.id
    user = await bot.fetch_user(int(userID))

    await user.send(tournamentRules)
    await ctx.send(format(ctx.message.author), "has successfully registered! Rules have been DMed!")

@bot.command(name='checkin')
async def checkin(ctx, challongeLink):
    hasDetails, loginDetails = await checkUserDetails(ctx)
    if not hasDetails:
        await ctx.send(
            'Please DM me your login details using ".userdetails email:password:username"! \nMessage will delete in 10 secs',
            delete_after=10)
        return

    session, authToken = login(loginDetails[0], loginDetails[1], False)
    checkIn(session, loginDetails[2], authToken, challongeLink)

    await ctx.send(format(ctx.message.author), "has successfully checked in!")

@bot.command(name='unregister')
async def unregistering(ctx, challongeLink):
    hasDetails, loginDetails = await checkUserDetails(ctx)
    if not hasDetails:
        await ctx.send(
            'Please DM me your login details using ".userdetails email:password:username"! \nMessage will delete in 10 secs',
            delete_after=10)
        return

    session, authToken = login(loginDetails[0], loginDetails[1], False)
    unregister(session, authToken, challongeLink)

    await ctx.send(format(ctx.message.author), "has successfully unregistered!")

bot.run(DISCORD_TOKEN)