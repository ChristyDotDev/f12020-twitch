# f12020-twitch

This project is to create a wee app which you can run alongside the game F1 2020 which will
allow you to make your telemetry data available on twitch streams via chat commands.


![alt jeffbot](https://i.imgur.com/ZU8l0eK.png)

## Pre-requisites

You'll need python installed. I've only tested it with Python 3.7.6

#### Bot account
You can run the bot using your own account but I'd recommend running it on a sub-account, means you can give it a nice name
and not worry about it streaming stuff to your account.

#### oauth token for Twitch IRC
https://dev.twitch.tv/console/apps/create - register the app here. Just set the oauth redirect to
http://localhost. Basically all you need from this is to grab the client ID. Keep this private

#### register the application with Twitch
https://twitchapps.com/tmi/ - connect your account here. Another reason to use a separate "bot" account is you don't have to connect
this to your main account. Keep the oauth token private

## Configuring the bot
Update the `.env` file with your config

## Enable telemetry in F1 2020
Make sure your settings are as below for UDP in the in-game settings.

![alt f1udpsettings](https://i.imgur.com/VrFOtkC.png)

You can tweak the send rate as you like but really, 10HZ is more than enough for this kinda telemetry. Nothing it's grabbing needs to be super up to date

```
# the oauth token we created on twitchapps
TMI_TOKEN=oauth:11111111111111111111
# the client ID for the application you registered on dev.twitch.tv  
CLIENT_ID=1111111111111111111111
# the username you will use. Either your bot account or your own
BOT_NICK=mybotsusername
# the prefix to trigger commands. I'd leave it as ! unless it's gonna clash with another bot
BOT_PREFIX=!
# the twitch channel you want it to connect to
CHANNEL=mytwitchchannel
```

## Running

On your PC, navigate to the project root and run:
```python
python bootstrapper.py
```
This kicks off 2 threads, one reads from the F12020 telemetry data stream and stores 
relevant data in memory, the other is a twitch bot which gives an API into this data.

You should see 2 messages if it's all started up successfully:
```
Listening to F1 telemetry
mybotsusername is online
```

## Twitch commands

`!standings` - outputs a horribly formatted list of the current race standings

`!tyres` - gives information about your tyres age and compound

`!fuel` - gives information on your current fuel mix and load 
