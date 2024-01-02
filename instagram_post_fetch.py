import asyncio
import instaloader
from dotenv import dotenv_values
import time, datetime
from utility import get_today_time_midnight
from discord_post import publish_post_to_discord

config = dotenv_values('.env')
values_str = config.get('INSTAGRAM_ACCOUNTS', '')
LOGIN_USERNAME = config.get('LOGIN_USERNAME', '')
LOGIN_PASSWORD = config.get('LOGIN_PASSWORD', '')
BASE_URL = 'https://www.instagram.com/p/'

check_time = 300 # in seconds (integer)

usernames = values_str.split(',') if values_str else [] 

L = instaloader.Instaloader()
L.login(LOGIN_USERNAME, LOGIN_PASSWORD)

# Define a dictionary to store last post timestamps for each username, defaulting to today's midnight for first run
last_post_timestamps = {username: datetime.datetime(2023, 12, 30) for username in usernames} 

async def main():

    while True:
        for username in usernames:

            last_post_timestamp = last_post_timestamps[username]
            print(username)
            user = instaloader.Profile.from_username(L.context, username)
            posts = user.get_posts() # gets all posts

            new_posts = []
            for post in posts:
                if post.date > last_post_timestamp:
                    new_posts.append(post)

            for new_post in new_posts:

                last_post_timestamps[username] = new_post.date

                post_id = new_post.shortcode

                post_data = {
                    'profile_name': new_post.owner_username,
                    'profile_image_url': new_post._owner_profile.profile_pic_url,
                    'post_description': new_post.caption,
                    'image_url': new_post.url,
                    'deep_link': f'{BASE_URL}{post_id}'
                }
                # Post to Discord channel
                await publish_post_to_discord(post_data)

                print(post_data['profile_name']), print(post_data['image_url']), print(post_data['post_description']), print(post_data['deep_link'])

        print('Power napping for 5 minutes...😴')

        await asyncio.sleep(check_time) # 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
