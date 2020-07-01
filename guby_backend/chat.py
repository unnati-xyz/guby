from rocketchat_API.rocketchat import RocketChat
import os
import logging
import traceback

logger = logging.getLogger(__name__)

rocket_admin = os.environ['ROCKET_ADMIN_USERNAME']
rocket_password = os.environ['ROCKET_ADMIN_PASSWORD']
rocket_host = os.environ['ROCKET_SERVER_HOST']
rocket_port = os.environ['ROCKET_SERVER_PORT']
server_url = 'http://' + rocket_host + ':' + rocket_port
rocket = RocketChat(rocket_admin, rocket_password, server_url=server_url)


def create_channel(channel_name: str) -> dict:
    '''
    This method takes channel name as input and returns a dict which contains messages and information regarding channel creation
    Use the dict['success'] to determine the channel creation
    '''
    try:
        channel_created = rocket.channels_create(channel_name).json()
        return channel_created
    except Exception as e:
        print(e)


if __name__ == "__main__":
    created_channel = create_channel('general')
    print(created_channel)
    created_channel = create_channel('test_guby')
    print(created_channel)

