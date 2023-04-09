from __future__ import annotations

import argparse
import asyncio
import os

from EdgeGPT import Chatbot

async def main() -> None:
    """
    Main function
    """
    print("Initializing...")
    print("Enter `alt+enter` or `escape+enter` to send a message")
    bot = Chatbot()
    while True:
        print("\nYou:")
        question = (
            input()
        )
        print()
        if question == "!exit":
            break
        if question == "!help":
            print(
                """
            !help - Show this help message
            !exit - Exit the program
            !reset - Reset the conversation
            """,
            )
            continue
        if question == "!reset":
            await bot.reset()
            continue
        print("Bot:")
        print(
            (
                await bot.ask(
                    prompt=question,
                    conversation_style=args.style,
                    wss_link=args.wss_link,
                )
            )["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"],
        )
    await bot.close()


if __name__ == "__main__":
    print(
        """
        !help for help
        !exit to exit
        !reset to reset conversation
        """,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--enter-once", action="store_true")
    parser.add_argument("--no-stream", action="store_true")
    parser.add_argument("--rich", action="store_true")
    parser.add_argument(
        "--proxy",
        help="Proxy URL (e.g. socks5://127.0.0.1:1080)",
        type=str,
    )
    parser.add_argument(
        "--wss-link",
        help="WSS URL(e.g. wss://sydney.bing.com/sydney/ChatHub)",
        type=str,
        default="wss://sydney.bing.com/sydney/ChatHub",
    )
    parser.add_argument(
        "--style",
        choices=["creative", "balanced", "precise"],
        default="balanced",
    )
    parser.add_argument(
        "--cookie-file",
        type=str,
        default="cookies.json",
        required=False,
        help="needed if environment variable COOKIE_FILE is not set",
    )
    args = parser.parse_args()
    if os.path.exists(args.cookie_file):
        os.environ["COOKIE_FILE"] = args.cookie_file
    else:
        parser.print_help()
        parser.exit(
            1,
            "ERROR: use --cookie-file or set environemnt variable COOKIE_FILE",
        )
    asyncio.run(main())

