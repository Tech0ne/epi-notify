from threading import Thread

import server
import bot

import sys

RUN_BOT_FIRST = True

def main():
    asnc_thread = bot.run if RUN_BOT_FIRST else server.run
    main_thread = server.run if RUN_BOT_FIRST else bot.run

    Thread(target=asnc_thread, daemon=True).start()

    try:
        main_thread()
    except Exception as e:
        print(f"Cought {e} while running main thread")
    return 0

if __name__ == "__main__":
    sys.exit(main())