import asyncio
import datetime
import os
from discord.utils import get
import discord
from discord import Embed, CategoryChannel
from discord.ext.commands import bot

from TicketState import Ticket, TicketState
from random_username.generate import generate_username

TOKEN = 'NzAyOTAwMzIxMzQ0Njg0MTEy.XxiaFQ.Z1j-TCa2QgH34nndJS5ObjuO6E0'
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

    print(message.author)
    role_names = [role.name for role in message.author.roles]
    name = str(message.channel)
    if 'client' in str(message.channel) and message.author.id != 702900321344684112:
        print('In client channel')
        actual_channel = str(message.channel).replace('client-', '')
        for channel in guild.channels:
            if 'scripter-' + actual_channel == str(channel):
                await message.guild.me.edit(nick='Client')
                await channel.send(message.content)
                await message.guild.me.edit(nick='Sichs Script Requester')

    if 'scripter' in str(message.channel) and message.author.id != 702900321344684112:
        print('In scripter channel')
        actual_channel = str(message.channel).replace('scripter-', '')
        for channel in guild.channels:
            if 'client-' + actual_channel == str(channel):
                await  message.guild.me.edit(nick='Scripter')
                await channel.send(message.content)
                await message.guild.me.edit(nick='Sichs Script Requester')

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
            # embed.add_field(name="Ticket User", value=f"{author}")
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
            # embed.add_field(name="Ticket User", value=f"{author}")
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
                        username = generate_username(1)
                        channel = await guild.create_text_channel('Client ' + str(username), overwrites=overwrites, category=category)
                        await channel.set_permissions(ticket.user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                        channel1 = await guild.create_text_channel('Scripter ' + str(username), overwrites=overwrites, category=category)
                        await channel1.set_permissions(user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                        new_embed = discord.Embed(title=f"{guild.name}", description=f"```{ticket.request}```",
                                                  timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                        # new_embed.add_field(name="Request User", value=f"{ticket.user}")
                        new_embed.add_field(name="Server ID", value=f"{guild.id}")
                        new_embed.set_footer(text="You will be communicating to a staff member via the bot. Please send a message!")
                        pfp = ticket.user.avatar_url
                        new_embed.set_thumbnail(url=pfp)
                        await channel.send(embed=new_embed)
                        await channel1.send(embed=new_embed)


                        new_embed = discord.Embed(title=f"{guild.name}", description=f"{ticket.request}",
                                              timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
                        # new_embed.add_field(name="Request User", value=f"{ticket.user}")
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