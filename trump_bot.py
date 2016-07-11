import os
import time
from slackclient import SlackClient

BOT_NAME = 'trumpbot'
BOT_ID = os.environ.get('BOT_ID')
AT_BOT = "<@" + BOT_ID + ">"

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    """
        Receives commands directed at Lord Trump and he answers them
    """
    response = "Look Crooked Yanir, I'm building a wall"
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
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading
    if slack_client.rtm_connect():
        print("TrumpBot is ready and waiting with the best answers")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Did those Mexicans build a wall?")
