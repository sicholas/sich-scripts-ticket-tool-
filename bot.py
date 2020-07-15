import asyncio
import datetime
import os
from discord.utils import get
import discord
from discord import Embed, CategoryChannel
from discord.ext.commands import bot

from TicketState import Ticket, TicketState

TOKEN = 'NzAyOTAwMzIxMzQ0Njg0MTEy.XvvYuA.AsOx9qN24Mmbp5iY91YnQ04PBfo'
GUILD = '682057230098628663'
client = discord.Client()
tickets = []

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} has connected to Discord!')
    print(f'{guild.name}(id: {guild.id})')


@client.event
async def on_message(message):
    print(message.channel.id)
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(message.author.roles)
    role_names = [role.name for role in message.author.roles]
    if message.content == "!archive" and "Scripter" in role_names:
        print("Archiving")
        channel = message.channel
        category = discord.utils.get(guild.categories, id=731843594708713553)
        await channel.edit(category=category)
    elif message.channel.id == 729922205106045069:
        ticket_created = False
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        for channel in guild.channels:
            if channel.name == message.author.display_name:
                ticket_created = True
                break
        if ticket_created == False:
            display = message.author.display_name
            author = message.author
            theMessage = message.content
            guild = message.guild
            await message.delete()
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }

            print(theMessage)
            embed = discord.Embed(title=f"{guild.name}", description=f"```{theMessage}```",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Ticket User", value=f"{author}")
            embed.add_field(name="Server ID", value=f"{guild.id}")
            embed.set_footer(text="👍 to accept || 👎 to decline")
            pfp = author.avatar_url
            embed.set_thumbnail(url=pfp)
            channel = client.get_channel(729923794881347585)
            admin_role = get(guild.roles, name="Scripter")
            await channel.send(admin_role.mention)
            sent = await channel.send(embed=embed)  # creates a message object called "sent"
            tickets.append(Ticket(sent, author, theMessage))
            await sent.add_reaction(emoji="\U0001F44D")  # use the message object to add the reaction to
            await sent.add_reaction(emoji="\U0001F44E")
            channel2 = await author.create_dm()
            embed = discord.Embed(title=f"{guild.name}", description=f"```{theMessage}```",
                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            embed.add_field(name="Ticket User", value=f"{author}")
            embed.add_field(name="Server ID", value=f"{guild.id}")
            embed.set_footer(text="Request Has Been Created, Please Wait for a Staff Member To Accept!")
            pfp = author.avatar_url
            embed.set_thumbnail(url=pfp)
            await channel2.send(embed=embed)

            var1 = discord.Embed(
                footer='Request Accepted',
                colour=discord.Colour.green()
            )

            @client.event
            async def on_reaction_add(reaction, user):
                # if reaction is not 'thumbs_up' return here
                # print(reaction.message)
                print(reaction)
                for ticket in tickets:
                    if (ticket.message.id == reaction.message.id and user.id != 702900321344684112 and str(reaction.emoji) == '👍'):
                        # ticket claimed by user
                        ticket.state = TicketState.CLAIMED
                        admin_role = get(guild.roles, name="Scripter")
                        category = discord.utils.get(guild.categories, id=731823656983855135)
                        # , category=category
                        channel = await guild.create_text_channel(ticket.user.display_name, overwrites=overwrites, category=category)
                        await channel.set_permissions(ticket.user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                        await channel.set_permissions(admin_role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                        new_embed = discord.Embed(title=f"{guild.name}", description=f"```{ticket.request}```",
                                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                        new_embed.add_field(name="Request User", value=f"{ticket.user}")
                        new_embed.add_field(name="Server ID", value=f"{guild.id}")
                        new_embed.set_footer(text="Script Has Been Accepted! Please wait for staff to assist you!")
                        pfp = ticket.user.avatar_url
                        new_embed.set_thumbnail(url=pfp)
                        await channel.send(embed=new_embed)

                        new_embed = discord.Embed(title=f"{guild.name}", description=f"{ticket.request}",
                                              timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                        new_embed.add_field(name="Request User", value=f"{ticket.user}")
                        new_embed.add_field(name="Server ID", value=f"{guild.id}")
                        new_embed.set_footer(text="Script Has Been Accepted By " + str(user))
                        pfp = ticket.user.avatar_url
                        new_embed.set_thumbnail(url=pfp)
                        await ticket.message.edit(embed=new_embed)
                        await channel.send(ticket.user.mention)
                        tickets.remove(ticket)
        else:
            await message.delete()


client.run(TOKEN)
