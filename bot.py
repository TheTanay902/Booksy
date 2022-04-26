from ast import Await

from matplotlib import image
from matplotlib.pyplot import colorbar, title
from dotenv import load_dotenv
from tabnanny import check
import discord
import os
from discord.ext import commands
from reccomendcommand import recbok
from discord.embeds import Embed
client = discord.Client()
client = commands.Bot(command_prefix="&")
is_client_running = False
load_dotenv()


@client.event
async def on_ready():
    global is_client_running

    if not is_client_running:
        is_client_running = True
        print(f"{client.user.name} is ready to go")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.command()
async def terminate(ctx):
    await ctx.send("Goodbye")
    await discord.Client().close()


@client.command()
async def hello(ctx):
    await ctx.send("Hey There, Ready for some recommendations?")


@client.command()
async def recommend(ctx, *bookname):
    if not bookname:
        return

    book = " ".join(bookname)
    mylist, urllist = recbok(book)
    await ctx.send(mylist[0])
    mylist.pop(0)
    for eachbook, eachurl in zip(mylist, urllist):
        smalleembed = Embed(title=eachbook, color=discord.Color.random())
        smalleembed.set_image(url=eachurl)
        await ctx.send(embed=smalleembed)


TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
