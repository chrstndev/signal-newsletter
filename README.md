# Signal Newsletter Bot
A bot that can be used to send multiple newsletters via Signal Messenger.

# Using the Bot 

To use the bot as a user it needs nothing more than a message with "start" to the number bound to the Signal CLI. 

As a user you will then be greeted with a welcome message with further instructions

Alternatively, you can sign up directly with a newsletter and can save the start message. This can be done by sending directly to the bot "subscribe < newsletter >".

To unsubscribe from a specific newsletter use "unsubscribe < newsletter >". To unsubscribe from all newsletters use "stop

## Known Issues
- If a user sends a message to the bot at the same moment as the bot processes the messages via GET request, the incoming message is not processed.
- Sending newsletters is currently only possible by calling a function within the script.



## Installation
To use the script you must have [signal-cli](https://github.com/AsamK/signal-cli) and [signal-cli-rest-api](https://github.com/bbernhard/signal-cli-rest-api) installed and have verified your number on the device. 

Deutsch: [Signal-cli & signal-cli-rest-api installation and usage](https://docs.google.com/document/d/1-k4Vxa6adzR_OtDZpeqVBNfi6nUxu6hWnhAF8tssfU8/edit?usp=sharing)

#### Requirements
This script requires
```
sqlite3
requests
json
```
You can install them by executing 
```
pip3 install -r requirements.txt
```

#### Declare variables
The file vars.json is used to save information and texts to avoid unnecessary long text lines in the script itself. To use this, the file vars.json.example must be renamed to vars.json and the variables must be filled in as follows:

- `source_number` is the number associated with the signal cli and used for sending and receiving messages. **Attention**: The number must also include the country code (example: +44123456789).
- `signal_api_url` The URL from the API [default of signal_cli_rest_api is localhost:8080]
- `available_newsletters` All newsletters you offer in one array 
- `available_newsletters_str` All Newsletters you offer in a String (Used when creating the Database)

##### Texts
- `newsletter_not_found` - Message that a user receives when the specified newsletter could not be found.
- `newsletter_subscribed` - Message a user receives when subscribing to a specific newsletter 
- `newsletter_unsubscribed` - Message a user receives when unsubscribing from a specific newsletter 
- `welcome_message` - Welcome message a user receives at the "Start" message
- `user_unsubscribed` - Message that a user receives when he uses "Stop". 
- `help_message` - Message that a user receives when he uses "help". 


#### Creating the Database
If there is no database yet you have to call the function create_new_database in the script

After filling in vars.json and creating the Database you are all set and can start the Script with `python bot.py`


## Sending Newsletters
Unfortunately it is not yet possible to send messages via e.g. a web dashboard messages can only be used via function call within the script

This is possible with the send_message function and the parameters (< newsletter_name >, < text >)