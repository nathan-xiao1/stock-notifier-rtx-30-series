import discord
import asyncio
from stores.StoreABC import Product
from StockNotifier import StockNotifier

CHANNEL_IDS = [807797016742461450]

stock_notifier = StockNotifier()
client = discord.Client()
channels = []

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    global channels
    channels = [client.get_channel(c_id) for c_id in CHANNEL_IDS]
    task = asyncio.create_task(stock_notifier.start())
    await task

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith("#"):
        for channel in channels:
            await client.get_channel(channel).send("Hello")
        # await message.channel.send(embed=createEmbedded(Product(name='MSI GeForce RTX 3070 VENTUS 2X OC 8GB Video Card', price='$1,049.00', store='Mwave', link='https://www.mwave.com.au/product/msi-geforce-rtx-3070-ventus-2x-oc-8gb-video-card-ac38099')))


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
        description=f"{'In stock' if in_stock else 'Out of stock'} now at {item.store}",
        color=0x4CAF50 if in_stock else 0xf50057
    )
    embed.set_thumbnail(url=item.image)
    embed.add_field(name="Price", value=item.price, inline=True)
    embed.add_field(name="Product Link",
                    value=f"[Take me there]({item.link})", inline=True)
    return embed

stock_notifier.registerCallback(notify)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(client.start('Njg3MTk2NTY4NDQwNTM3MDk4.XmiPrQ.cQ9offaNNdY-75r3ckBw49qZkSQ'))
except KeyboardInterrupt:
    loop.run_until_complete(client.logout())
finally:
    stock_notifier.save()
    loop.close()

