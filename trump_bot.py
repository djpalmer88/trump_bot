import os
import time
import aiml
from slackclient import SlackClient

BOT_NAME = 'trumpbot'
BOT_ID = os.environ.get('BOT_ID')
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
api_call = slack_client.api_call("users.list")
users = api_call.get("members")
username_dicts = [{user["id"]: user["name"]} for user in users]
usernames = {}
for username in username_dicts:
    for key, value in username.items():
        if value == "yanir":
            username[key] = "tanir"
    usernames.update(username)

k = aiml.Kernel()
k.learn("std-startup.xml")
k.respond("LOAD BASIC CHAT")
print(usernames)

def handle_command(command, channel, user_name):
    """
        Receives commands directed at Lord Trump and he answers them
    """
    print(user_name)
    response = k.respond(user_name.capitalize() + " " + command)
    if not response:
        response = "Look %s, I don't know what you're trying to say and I don't care" % user_name.capitalize()
    response = process_final_response(response)
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        Reads messages in real time and returns commands and channel
        if they are directed at Lord Trump
    """
    print(slack_rtm_output)
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel'], usernames[output['user']]
    return None, None, None

def process_final_response(response):
    return response.replace("yanir", "tanir")
    
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading
    if slack_client.rtm_connect():
        print("TrumpBot is ready and waiting with the best answers")
        while True:
            command, channel, user_name = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, user_name)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Time to build a wall?")
