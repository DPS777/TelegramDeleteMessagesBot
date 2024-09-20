import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv, set_key
from pathlib import Path
from enum import Enum
import asyncio

CONFIG_FOLDER = 'config'

class TelegramBot:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient(os.path.join(CONFIG_FOLDER, 'session_' + phone_number), api_id, api_hash)

    async def list_chats(self):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        # Get a list of all the dialogs (chats)
        dialogs = await self.client.get_dialogs()
        chats_file = open(str(os.path.join(CONFIG_FOLDER,f"chats_of_{self.phone_number}.txt")), "w", encoding="utf-8")
        # Print information about each chat
        for dialog in dialogs:
            print(f"Chat ID: {dialog.id}, Title: {dialog.title}")
            chats_file.write(f"Chat ID: {dialog.id}, Title: {dialog.title} \n")
          
        print("List of groups printed successfully!")

    async def delete_messages(self, chat_id, message_ids):

        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        # Delete the messages
        await self.client.delete_messages(chat_id, message_ids)
        print("Messages deleted successfully!")

    async def get_messages(self, chat_id, limit, reverse, min_id=None, max_id=None, ids=None):

        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        # Get the messages
        if min_id is not None and max_id is not None:
            messages_ids = await self.client.get_messages(chat_id, limit=limit, reverse=reverse, min_id=min_id, max_id=max_id)
        elif ids is not None:
            messages_ids = await self.client.get_messages(chat_id, limit=limit, reverse=reverse, ids=ids)
        else:
            messages_ids = await self.client.get_messages(chat_id, limit=limit, reverse=reverse)

        return messages_ids

# Function to read credentials from .env file
def read_credentials():
    try:
        load_dotenv(Path(os.path.join(CONFIG_FOLDER, ".env")))
        api_id = os.getenv('API_ID')
        api_hash = os.getenv('API_HASH')
        phone_number = os.getenv('PHONE_NUMBER')
        return api_id, api_hash, phone_number
    except Exception as e:
        print("Error reading .env file:", str(e))
        return None, None, None
    
# Function to write credentials to .env file
def write_credentials(api_id, api_hash, phone_number):
    env_file_path = Path(os.path.join(CONFIG_FOLDER, ".env"))
    env_file_path.touch(mode=0o600, exist_ok=False)
    set_key(dotenv_path=env_file_path, key_to_set="API_ID", value_to_set=api_id)
    set_key(dotenv_path=env_file_path, key_to_set="API_HASH", value_to_set=api_hash)
    set_key(dotenv_path=env_file_path, key_to_set="PHONE_NUMBER", value_to_set=phone_number)

def remove_type_MessageService(array):

    for element in array:
        if type(element).__name__ != 'Message':
            array.remove(element)

async def choose_type_delete(bot, chat_id):

    while True:
        print("Choose a type of message to delete:")
        print("1. Delete all messages")
        print("2. Delete from the oldest to the newest (numbers)")
        print("3. Delete from the newest to the oldest (numbers)")
        print("4. Delete from a range of message IDs (message IDs)")
        print("5. Delete a specific message (number)")
        print("6. Delete a specific message (message ID)")
        print("7. Exit")

        choice = input("Enter your choice: ")

        confirm = input("Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            continue

        if choice == '1':
            message_ids = await bot.get_messages(chat_id, limit=None, reverse=False)
            remove_type_MessageService(message_ids)
            await bot.delete_messages(chat_id, message_ids)
        elif choice == '2':
            message_ids = await bot.get_messages(chat_id, limit=None, reverse=True)
            remove_type_MessageService(message_ids)

            start = int(input("Enter the start of the range (values start from 1 and end at the number of messages, inclusive): "))
            end = int(input("Enter the end of the range (values start from 1 and end at the number of messages, inclusive): "))

            while start < 1 or end < 1 or start > end or start > len(message_ids) or end > len(message_ids):
                print("Invalid range. Please try again. Confirm if the range is correct and if start is less than end.")
                start = int(input("Enter the start of the range (values start from 1 and end at the number of messages, inclusive): "))
                end = int(input("Enter the end of the range (values start from 1 and end at the number of messages, inclusive): "))

            message_ids = message_ids[start-1:end] # -1 because lists are 0-indexed and end is + 1 - 1
            await bot.delete_messages(chat_id, message_ids)
        elif choice == '3':
            message_ids = await bot.get_messages(chat_id, limit=None, reverse=False)
            remove_type_MessageService(message_ids)

            start = int(input("Enter the start of the range (values start from 1 and end at the number of messages, inclusive): "))
            end = int(input("Enter the end of the range (values start from 1 and end at the number of messages, inclusive): "))

            while start < 1 or end < 1 or start > end or start > len(message_ids) or end > len(message_ids):
                print("Invalid range. Please try again. Confirm if the range is correct and if start is less than end.")
                start = int(input("Enter the start of the range (values start from 1 and end at the number of messages, inclusive): "))
                end = int(input("Enter the end of the range (values start from 1 and end at the number of messages, inclusive): "))

            message_ids = message_ids[start-1:end] # -1 because lists are 0-indexed and end is + 1 - 1
            await bot.delete_messages(chat_id, message_ids)
        elif choice == '4':
            message_idsasd = await bot.get_messages(chat_id, limit=None, reverse=True)
            remove_type_MessageService(message_idsasd)

            print(message_idsasd)

            start = int(input("Enter the start of the range (smaller message ID, inclusive): "))
            end = int(input("Enter the end of the range (larger message ID, inclusive): "))

            while start > end:
                print("Invalid range. Please try again. Confirm if the range is correct and if start is less than end.")
                start = int(input("Enter the start of the range (smaller message ID, inclusive): "))
                end = int(input("Enter the end of the range (larger message ID, inclusive): "))

            message_ids = await bot.get_messages(chat_id, limit=None, min_id=start-1, max_id=end+1, reverse=True)
            remove_type_MessageService(message_ids)   
            await bot.delete_messages(chat_id, message_ids)
            
        elif choice == '5':
            message_ids = await bot.get_messages(chat_id, limit=None, reverse=False)
            remove_type_MessageService(message_ids)

            message_number = int(input("Enter the message number to delete (from newest to oldest): "))

            while message_number < 1 or message_number > len(message_ids):
                print("Invalid message number. Please try again.")
                message_number = int(input("Enter the message number to delete (from newest to oldest): "))

            await bot.delete_messages(chat_id, [message_ids[message_number-1]])
        elif choice == '6':
            message_id = int(input("Enter the message ID to delete: "))

            message_ids = await bot.get_messages(chat_id, limit=None, reverse=False, ids=message_id)

            await bot.delete_messages(chat_id, message_ids)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

async def main():

    # Create config folder if it doesn't exist
    if not os.path.exists(CONFIG_FOLDER):
        os.makedirs(CONFIG_FOLDER)

    # Attempt to read credentials from .env file
    api_id, api_hash, phone_number = read_credentials()

    # If credentials not found in .env file, prompt the user to input them
    if api_id is None or api_hash is None or phone_number is None:
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API Hash: ")
        phone_number = input("Enter your phone number: ")
        # Write credentials to .env file for future use
        write_credentials(api_id, api_hash, phone_number)

    bot = TelegramBot(api_id, api_hash, phone_number)

    print("Choose an option:")
    print("1. List Chats")
    print("2. Delete Messages")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        await bot.list_chats()
    elif choice == '2':
        
        continuar = True

        while continuar:

            chat_id = int(input("Enter the chat ID: "))
            await choose_type_delete(bot, chat_id)
            print("Do you want to continue and choose another chat? (Y/n)")
            continuar = input().lower() != 'n'

    elif choice == '3':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Exiting...")
        return

    await bot.client.disconnect()

# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())