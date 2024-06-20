import os
import re
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import ChannelInvalidError
import config

# Initialize the Telegram client
client = TelegramClient('session_name', config.api_id, config.api_hash)

# Helper function to create log file path
def get_log_file_path(group_name):
    date_str = datetime.now().strftime('%Y-%m')
    log_file_name = f"log_{group_name}_{date_str}.log"
    return log_file_name

# Define the event handler for new messages
@client.on(events.NewMessage)
async def handler(event):
    message_text = event.message.message
    if any(re.search(rf'\b{name}\b', message_text, re.IGNORECASE) for name in config.thailand_names):
        sender = await event.get_sender()
        chat = await event.get_chat()
        group_name = chat.username or chat.title.replace(' ', '_')
        log_file_path = get_log_file_path(group_name)
        log_entry = f"""Message in {group_name} from {sender.username} @ {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}:
        
\"\"\"
{message_text}
\"\"\"

"""
        
        # Log the message to the respective log file
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry)
        
        print(f"Logged message from {sender.username} in {chat.title}")

async def main():
    # Start the client
    await client.start(config.phone_number)

    # Join all the groups
    for group_url in config.groups:
        group_name = group_url.split('/')[-1]
        try:
            await client(JoinChannelRequest(group_name))
            print(f"Joined group: {group_name}")
        except ChannelInvalidError:
            print(f"Failed to join group {group_name}: Invalid group")
        except Exception as e:
            print(f"Failed to join group {group_name}: {e}")

    # Run the client until disconnected
    await client.run_until_disconnected()

# Run the client
client.loop.run_until_complete(main())
