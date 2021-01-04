import os
from twitchio.ext import commands
from dotenv import load_dotenv
from telemetry.telemetry_listener import get_standings

load_dotenv()

# set up the bot
bot = commands.Bot(
    irc_token=os.environ["TMI_TOKEN"],
    client_id=os.environ["CLIENT_ID"],
    nick=os.environ["BOT_NICK"],
    prefix=os.environ["BOT_PREFIX"],
    initial_channels=[os.environ["CHANNEL"]]
)


@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f'{os.environ["BOT_NICK"]} is online')
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ["CHANNEL"], f"/me has landed!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    # make sure the bot ignores itself
    if ctx.author.name.lower() == os.environ["BOT_NICK"].lower():
        return

    await bot.handle_commands(ctx)

    await ctx.channel.send(ctx.content)

    if 'hello' in ctx.content.lower():
        await ctx.channel.send(f"Hi, @{ctx.author.name}!")


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong!')


@bot.command(name='leader')
async def leader(ctx):
    standings = get_standings()
    if standings is not None:
        await ctx.send(f"{standings[1]['driver'].name.decode('utf-8')} is in the lead")
    else:
        print("No standings")


def start_bot():
    bot.run()
