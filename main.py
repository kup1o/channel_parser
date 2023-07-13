from bs4 import BeautifulSoup
import aiogram
import os
import requests

# Get the bot token from environment variables
bot_token = os.environ.get('BOT_TOKEN')

# Create an instance of the bot
bot = aiogram.Bot(token=bot_token)
dp = aiogram.Dispatcher(bot)

# Handler for the "/start" command
@dp.message_handler(commands=['start'])
async def start(message: aiogram.types.Message):
    await message.reply("Welcome! Please enter the variable ID:")

# Handler for text messages
@dp.message_handler(content_types=aiogram.types.ContentTypes.TEXT)
async def process_text(message: aiogram.types.Message):
    variable_id = message.text.strip()
    url = f"https://t.me/s/{variable_id}"

    # Make a GET request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the div elements with the specified classes
    class_names = ["tgme_channel_info_header_title", "tgme_channel_info_header_username"]
    results = []

    for class_name in class_names:
        element = soup.find("div", class_=class_name)
        if element:
            results.append(element.text.strip())
        else:
            results.append(f"Div element with class '{class_name}' not found.")

    # Send the results as a message to the user
    await message.reply("\n".join(results))

# Start the bot
if __name__ == '__main__':
    aiogram.executor.start_polling(dp)
