# Telegram-Scraper
The telegram scraper reads using the Telethon API, making an instance of a message in Telegram visible to a Discord group. Useful for communities which require Telegram chat history to be saved in Discord, to utilise the unique Discord search functionality. 

The scraper will connect to a channel on Telegram via login through the Telegram developer portal, the chat history is saved in mySQL so the host server has a history of messages, which can be used to extend additional functionality, such as reply messages.  

Useful documentation: <br>
https://docs.telethon.dev/en/stable/ <br>
https://stackoverflow.com/questions/69388729/scraping-telegram-messages-in-telethon-using-channel-id <br>
