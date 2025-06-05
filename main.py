from typing import Final
import os
from dotenv import load_dotenv 
from discord import Intents, Client, Message
from responses import get_response


#STEP 0: LOAD TOKEN FROM SOMEWHERE SAFE
load_dotenv()

TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#STEP 1: SET UP THE BOT
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

#STEP 1: message functionality

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("(Message was empty because intents were not enabled maybe)")
        return
    
    is_private = user_message[0:5] == "?ouou" 
    if is_private:
        user_message = user_message[1:]

    try:
        user_id = str(message.author.id)  # Get the user's ID
        response: str = get_response(user_message, user_id)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(f"Error sending message: {e}")

#STEP 3: handling bot startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

#STEP 4: handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    username: str =str(message.author)

    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

#STEP 5: main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
