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
    print(f'{os.environ["BOT_NICK"]} is online!')
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ["CHANNEL"], f"/me has landed!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    print("Detected message")

    # make sure the bot ignores itself and the streamer
    # if ctx.author.name.lower() == os.environ["BOT_NICK"].lower():
    #    return

    print(bot.commands)
    await bot.handle_commands(ctx)

    # await ctx.channel.send(ctx.content)

    if 'hello' in ctx.content.lower():
        await ctx.channel.send(f"Hi, @{ctx.author.name}!")


@bot.command(name='ping')
async def ping(ctx):
    print("DETECTED MESSAGE")
    await ctx.send('pong!')


@bot.command(name='leader')
async def leader(ctx):
    print("DETECTED STANDINGS MESSAGE")
    standings = get_standings()
    print(standings[1]['driver'])
    await ctx.send(f"{standings[1]['driver'].name.decode('utf-8')} is in the lead" )


def start_bot():
    bot.run()
