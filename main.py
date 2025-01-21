import discord
import os
import sys
import asyncio
from config import BOT_TOKEN
from config import PATH_TO_WORDS

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


with open(PATH_TO_WORDS, 'r') as file:
    words = file.read().split()


@client.event
async def on_ready():
    print(bcolors.OKGREEN + "Ready to Censor" + bcolors.ENDC)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the message is from any webhook other than the Censor webhook
    censor_webhook = await get_or_create_webhook(message.channel)
    if not message.webhook_id or message.webhook_id != censor_webhook.id:
        censored_message = message.content
        for word in words:
            if word in message.content.lower():
                censored_message = censored_message.replace(word, f'||{word}||')
        
        if censored_message != message.content:
            avatar_url = message.author.avatar.url if isinstance(message.author.avatar, discord.Asset) else discord.Embed.Empty
            await censor_webhook.send(censored_message, username=message.author.display_name, avatar_url=avatar_url)
            await message.delete()

async def get_or_create_webhook(channel):
    webhooks = await channel.webhooks()
    for webhook in webhooks:
        if webhook.name == "Censor":
            return webhook
    # If no webhook is found, create a new one
    return await channel.create_webhook(name="Censor")


async def shutdown():
    await client.close()

try:
    client.run(BOT_TOKEN)  # Load the bot token from the environment variable
except KeyboardInterrupt:
    asyncio.run(shutdown())
    print("Bot is shutting down...")
    sys.exit(42)
