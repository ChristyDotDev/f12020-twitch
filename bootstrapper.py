from twitch_bot import bot
from telemetry import telemetry_listener

import threading

# Daemonize the telemetry thread and kick it off
telemetry_thread = threading.Thread(target=telemetry_listener.run_telemetry, args=())
telemetry_thread.daemon = True
telemetry_thread.start()

bot.start_bot()
