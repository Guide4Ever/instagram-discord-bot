import discord
from dotenv import dotenv_values
#from utility.dummy_data import post_data
import asyncio

post_data = {
    'profile_name': 'test_user',
    'profile_image_url': 'https://images.pexels.com/photos/771742/pexels-photo-771742.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',
    'post_description': 'This is a test post',
    'image_url': 'https://www.adorama.com/alc/wp-content/uploads/2018/11/landscape-photography-tips-yosemite-valley-feature.jpg',
    'deep_link': 'https://www.instagram.com'
}

config = dotenv_values('.env')
BOT_TOKEN = config.get('BOT_TOKEN', '')
CHANNEL_ID = int(config.get('CHANNEL_ID', ''))  # Ensure CHANNEL_ID is converted to int

async def publish_post_to_discord(post_data):
    profile_name = post_data["profile_name"]
    profile_image_url = post_data["profile_image_url"]
    post_description = post_data["post_description"]
    image_url = post_data["image_url"]
    deep_link = post_data["deep_link"]

    # Create an async function to handle the Discord bot and posting logic
    async def post_to_discord():
        # Create a Discord client with intents
        
        client = discord.Client(intents=discord.Intents.all())

        @client.event
        async def on_ready():
            # Once the client is ready, get the channel to post to
            channel = client.get_channel(CHANNEL_ID)
            
            # Create an embed object for the post
            embed = discord.Embed(
                title="@" + profile_name,
                url=deep_link,
                color=discord.Color.green(),
                description=post_description
            )

            # Set the author of the embed
            embed.set_author(name=profile_name, url=deep_link, icon_url=profile_image_url)

            # Set the main image of the embed
            embed.set_image(url=image_url)

            # Post the embed message to the channel
            await channel.send(embed=embed)

        await client.start(BOT_TOKEN)

    # Run the async function within an event loop
    try:
        await post_to_discord()
    except Exception as e:
        print(f"An error occurred: {e}")

# Create an event loop to run the async function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(publish_post_to_discord(post_data))
