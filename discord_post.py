import discord
from dotenv import dotenv_values

config = dotenv_values('.env')
BOT_TOKEN = config.get('BOT_TOKEN', '')
CHANNEL_ID = config.get('CHANNEL_ID', '')

async def publish_post_to_discord(post_data):
    profile_name = post_data["profile_name"]
    profile_image_url = post_data["profile_image_url"]
    post_description = post_data["post_description"]
    image_url = post_data["image_url"]
    deep_link = post_data["deep_link"]

    # Create a Discord client with intents
    client = discord.Client(intents=discord.Intents.all())
    client.run(BOT_TOKEN)

    @client.event
    async def on_ready():
        # Once the client is ready, get the channel to post to
        channel = client.get_channel(CHANNEL_ID)
        print(f"Posting to channel: {channel}")
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

    