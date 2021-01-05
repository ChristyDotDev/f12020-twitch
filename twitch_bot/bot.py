import os
from twitchio.ext import commands
from dotenv import load_dotenv
from telemetry.telemetry_listener import get_standings, get_player_status, tyre_compounds

load_dotenv()

for key in ["TMI_TOKEN", "CLIENT_ID", "BOT_NICK", "BOT_PREFIX", "CHANNEL"]:
    if os.getenv(key) is None:
        print(f"{key} must be set in env")
        exit(1)

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
    print(f'{os.environ["BOT_NICK"]} is online')
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ["CHANNEL"], f"/me has landed!")


@bot.event
async def event_message(ctx):
    # TODO - for now the bot doesn't ignore itself. This is just so you can run it on your own account without needing a "bot" sub-account
    # if ctx.author.name.lower() == os.environ["BOT_NICK"].lower():
    #    return

    await bot.handle_commands(ctx)


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong!')


@bot.command(name='leader')
async def leader(ctx):
    standings_obj = get_standings()
    if standings_obj is not None:
        await ctx.send(f"{standings_obj[1]['driver'].name.decode('utf-8')} is in the lead")
    else:
        print("No standings")


@bot.command(name='standings')
async def standings(ctx):
    standings_obj = get_standings()
    if standings_obj is not None:
        standings_string = ""
        for i in range(1, len(standings_obj) + 1):
            standings_string += f"P{i}: {standings_obj[i]['driver'].name.decode('utf-8')}\n"
        await ctx.send(f"Standings:\n{standings_string}")
    else:
        print("No standings")


@bot.command(name='fuel')
async def fuel(ctx):
    player_status = get_player_status()
    if player_status is not None:
        fuel_string = f"Mix {player_status.fuelMix}, laps: {round(player_status.fuelRemainingLaps, 2)}," \
                      f" in tank: {round(player_status.fuelInTank, 2)}L"
        await ctx.send(f"Fuel:\n{fuel_string}")
    else:
        print("No player status")


@bot.command(name='tyres')
async def tyres(ctx):
    player_status = get_player_status()
    if player_status is not None:
        tyres_string = f"age {player_status.tyresAgeLaps} laps," \
                       f" compound: {tyre_compounds[player_status.actualTyreCompound]}"
        await ctx.send(f"Tyres:\n{tyres_string}")
    else:
        print("No player status")


def start_bot():
    bot.run()
