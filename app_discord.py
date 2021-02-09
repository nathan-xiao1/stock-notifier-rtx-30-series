import asyncio
import argparse
import discord
import pytz
from stores.StoreABC import Product
from StockNotifier import StockNotifier
from datetime import datetime

ADMIN = [208546713458311168]
CHANNEL_IDS = [807797016742461450]
TIME_FORMAT = '%I:%M %p %d/%m/%Y '
TIME_ZONE = pytz.timezone('Australia/Sydney')

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", metavar="debug",
                    type=bool, help="enable debug mode")
args = parser.parse_args()

stock_notifier = StockNotifier()
client = discord.Client()
channels = []


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    global channels
    channels = [client.get_channel(c_id) for c_id in CHANNEL_IDS]
    if not args.debug:
        try:
            task = asyncio.create_task(stock_notifier.start())
            await task
        except KeyboardInterrupt:
            print("Terminating stock notifier")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.author.id in ADMIN and message.content.startswith("!!"):
        print(f"{message.author}: {message.content}")
        if message.content == "!!clear" and message.channel in channels:
            await message.channel.send('Confirm clear message? (y/n)')
            msg = await client.wait_for('message')
            if msg.content != "y":
                return
            await message.channel.delete_messages(await message.channel.history().flatten())
        elif message.content == "!!embed":
            await message.channel.send(embed=createEmbedded(
                Product(
                    name='MSI GeForce RTX 3070 VENTUS 2X OC 8GB Video Card',
                    price='$1,049.00',
                    image='https://cdn.mwave.com.au/images/midimage/msi_geforce_rtx_3070_ventus_2x_oc_8gb_video_card_ac38099_1.jpg',
                    store='Mwave',
                    link='https://www.mwave.com.au/product/msi-geforce-rtx-3070-ventus-2x-oc-8gb-video-card-ac38099')
                )
            )


async def notify(in_stock, out_stock):
    print("Notified")
    for item in in_stock:
        for channel in channels:
            await channel.send(embed=createEmbedded(item))
    for item in out_stock:
        for channel in channels:
            await channel.send(embed=createEmbedded(item, in_stock=False))


def createEmbedded(item, in_stock=True):
    embed = discord.Embed(
        title=item.name,
        description=f"{'In stock' if in_stock else 'Out of stock'} now at **{item.store}**",
        color=0x4CAF50 if in_stock else 0xf50057
    )
    embed.set_thumbnail(url=item.image)
    embed.add_field(name="Price", value=item.price, inline=True)
    embed.add_field(name="Product Link",
                    value=f"[Take me there]({item.link})", inline=True)
    embed.set_footer(
        text=f"Updated at {datetime.now(TIME_ZONE).strftime(TIME_FORMAT)}")
    return embed


stock_notifier.registerCallback(notify)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(client.start(
        'Njg3MTk2NTY4NDQwNTM3MDk4.XmiPrQ.cQ9offaNNdY-75r3ckBw49qZkSQ'))
except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
finally:
    stock_notifier.save()
    loop.close()
