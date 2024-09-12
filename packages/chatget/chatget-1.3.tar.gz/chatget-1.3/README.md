# chatGET
## _the simplest way to get a twitch chat into your project_




## How to Use

- Connect to Twitch via the command 'run_chat_server'
- Get the next chat message from a queue of messages using 'get_next_chat'
- That's it!

## Functions
1. run_chat_server(broadcaster_id, auth_token, user_id, client_id)
    - Connects to the Twitch API websocket on a thread
2. get_next_chat()
    - Returns either "None" (if no more chat activity) or a string containing the next chat in chronological order from the time that run_chat_server was called! 

## Example Usage
Here's some example code that will reproduce the contents of a broadcaster's Twitch chat in your console!
```sh
import chatget
import time

broadcaster_id = "ID of user who's chat you want to grab"
auth_token = "auth token from twitch" # TODO : more instruction on this"
user_id = "ID of the user who's grabbing chat (You)"
client_id = "ID of the bot that's using this library, registered on Twitch for Developers" 

run_chat_server(broadcaster_id, auth_token, user_id, client_id)

while True:
    msg = get_next_chat_msg()
    if(msg is not None): 
        print(msg)
    time.sleep(1)
```

