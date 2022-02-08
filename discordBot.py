# bot.py
import os
import mysql.connector
from random import randint, randrange
import datetime
import asyncio


import discord
from dotenv import load_dotenv

from discord.ext import commands
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

intents = discord.Intents.default()  # Allow the use of custom intents
intents.members = True

bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('with you, helping you win'))


@bot.command(name = 'connected', help = "Responds if the bot is running and connected to the server")
async def connected(ctx):

    confirmConnected = 'AutoVision is connected'

    response = confirmConnected
    await ctx.send(response)



modList = [629822062776680459, 262197748181368832, 210538210114142208, 439869066669195274] # jaj, JOE-B, Mad, dricon


dbList = ['2k22', 'mlb', 'wz', 'van', 'halo']

def getDB(dbname):
    if dbname == '2k21':
        db = mysql.connector.connect(
            host="h",
            user="u",
            password="p",
            database="2k21"
        )
    elif '2k' in dbname:
        db = mysql.connector.connect(
            host="h",
            user="u",
            password="p",
            database="2k22"
        )
    elif 'mlb' in dbname:
        db = mysql.connector.connect(
            host="h",
            user="u",
            password="p",
            database="mlb21"
        )
    elif dbname == 'wz':
        db = mysql.connector.connect(
            host="h",
            user="u",
            password="p",
            database="warzone"
        )
    elif dbname == 'van':
        db = mysql.connector.connect(
            host="h",
            user="u",
            password="p",
            database="vanguard"
        )
    elif dbname == 'halo':
        db = mysql.connector.connect(
            host="h",
            user="u",
            password="p",
            database="haloinf"
        )
    elif dbname == 'template':
        db = mysql.connector.connect(
            host="h",
            user="u",
            password="p",
            database="template"
        )
    elif dbname == 'bf':
        db = mysql.connector.connect(
            host="h",
            user="u",
            password="p",
            database="bf"
        )
    else:
        db = 0

    return db

def checkMod(ctx):
    return ctx.author.id in modList

def checkUserObject(user):
    return "@" in user


#CHECK USER ACCOUNT
@bot.command(name = 'inspect', help = "Check all user's info")
async def inspect(ctx, user):
    if "-help-" in ctx.message.channel.name or "vision-" in ctx.message.channel.name:
        if checkUserObject(user):
            if checkMod(ctx):

                username = ctx.message.mentions[0].name
                discriminator = ctx.message.mentions[0].discriminator
                combinedName = username + "#" + discriminator
                discordid = ctx.message.mentions[0].id

                for database in dbList:
                    db = getDB(database)
                    cursor = db.cursor()
                    try:
                        sql = "SELECT id FROM members WHERE discordid = %s"
                        val = (discordid,)
                        cursor.execute(sql, val)
                        id = cursor.fetchall()
                        id = id[0][0]

                        try:
                            sql = "SELECT subscription FROM members WHERE discordid = %s"
                            val = (discordid,)
                            cursor.execute(sql, val)
                            sub = cursor.fetchall()
                            sub = sub[0][0]
                            if sub == None:
                                sub = 'lifetime'
                        except:
                            sub = 'lifetime'

                        sql = "SELECT totaltime FROM members WHERE discordid = %s"
                        val = (ctx.message.mentions[0].id,)
                        cursor.execute(sql, val)
                        result = cursor.fetchall()
                        result = result[0][0]

                        await ctx.send("{}: ID: {}, subscription: {}, played: {} minutes".format(database, id, sub, result))
                    except:
                        print("{} does not exist in {}".format(combinedName, database))
            else:
                await ctx.send("You are not authorized to use that command")
        else:
            await ctx.send("Invalid user parameter")


#USER RESET HWID COMMAND
@bot.command(name = 'reset', help = "Reset your current hwid locked ID")
async def resethwid(ctx):
    if "-help-" in ctx.message.channel.name or "vision-" in ctx.message.channel.name:
        username = ctx.message.author.name
        discriminator = ctx.message.author.discriminator
        combinedName = username + "#" + discriminator
        print("reset used by {}".format(username))

        for database in dbList:
            db = getDB(database)
            try:
                cursor = db.cursor()
                sql = "UPDATE members SET hwid = %s WHERE discordid = %s"
                val = (None, ctx.message.author.id)
                cursor.execute(sql, val)
            except Exception as e:
                print(e)
        await ctx.send("Cleared hwid for {}".format(combinedName))



#CREATE NEW USER COMMAND
@bot.command(name = 'newUser', help = "Add a new user to the selected database, returns an ID for the user")
async def newUser(ctx, user, db):
    if "-help-" in ctx.message.channel.name or "vision-" in ctx.message.channel.name:
        if checkUserObject(user):
            if checkMod(ctx):
                try:
                    username = ctx.message.mentions[0].name
                    discriminator = ctx.message.mentions[0].discriminator
                    combinedName = username + "#" + discriminator
                    discordid = ctx.message.mentions[0].id
                    print("newUser({}, {}) used by {}".format(combinedName, db, ctx.author.name))
                except:
                    await ctx.send("Invalid user parameter")
                    return

                randomID = randrange(10000, 99999)

                database = getDB(db)
                if database == 0:
                    await ctx.send("That database does not exist")
                else:
                    try:
                        cursor = database.cursor()
                        sql = "INSERT INTO members (id, discord, discordid) VALUES (%s, %s, %s)"
                        val = (randomID, combinedName, discordid)
                        cursor.execute(sql, val)

                        await ctx.send("{} added, ID: {}".format(combinedName, randomID))
                        member = ctx.message.mentions[0]
                        if '2k' in db:
                            role = get(member.guild.roles, name="Vision")
                            await member.add_roles(role)
                    except Exception as e:
                        await ctx.send(e)
            else:
                await ctx.send("You are not authorized to use that command")
        else:
            await ctx.send("Invalid user parameter")


#REMOVE USER COMMAND
@bot.command(name = 'removeUser', help = "Remove a user entry, including their ID from the database")
async def removeUser(ctx, user, db):
    if "-help-" in ctx.message.channel.name or "vision-" in ctx.message.channel.name:
        if checkUserObject(user):
            if checkMod(ctx):
                try:
                    username = ctx.message.mentions[0].name
                    discriminator = ctx.message.mentions[0].discriminator
                    combinedName = username + "#" + discriminator
                    print("removeUser({}, {}) used by {}".format(combinedName, db, ctx.author.name))
                except:
                    await ctx.send("Invalid user parameter")
                    return

                db = getDB(db)
                if db == 0:
                    await ctx.send("That database does not exist")
                else:
                    try:
                        cursor = db.cursor()
                        sql = "DELETE FROM members WHERE discordid = %s;"
                        val = (ctx.message.mentions[0].id, )
                        cursor.execute(sql, val)

                        await ctx.send("Deleted {}".format(combinedName))
                    except:
                        await ctx.send("User does not exist")
            else:
                await ctx.send("You are not authorized to use that command")
        else:
            await ctx.send("Invalid user parameter")



#USER GET THEIR ID
@bot.command(name = 'getID', help = "Get your current ID")
async def getID(ctx):
    if "-help-" in ctx.message.channel.name or "vision-" in ctx.message.channel.name:
        username = ctx.message.author.name
        discriminator = ctx.message.author.discriminator
        combinedName = username + "#" + discriminator
        print("getID() used by {}".format(ctx.author.name))

        for database in dbList:
            db = getDB(database)
            cursor = db.cursor()
            try:
                sql = "SELECT id FROM members WHERE discordid = %s"
                val = (ctx.message.author.id,)
                cursor.execute(sql, val)
                result = cursor.fetchall()
                result = result[0][0]

                await ctx.send("{} ID is {} for {}".format(combinedName, result, database))
            except:
                print("{} does not exist in {}".format(combinedName, database))



#GET SUBSCRIPTION EXPIRY DATE
@bot.command(name = 'getSub', help = "Get the current subscription expiry date for the user")
async def getSub(ctx, user, db):
    if "-help-" in ctx.message.channel.name or "vision-" in ctx.message.channel.name:
        if checkUserObject(user):
            if checkMod(ctx):
                try:
                    username = ctx.message.mentions[0].name
                    discriminator = ctx.message.mentions[0].discriminator
                    combinedName = username + "#" + discriminator
                    print("getSub({}, {}) used by {}".format(combinedName, db, ctx.author.name))
                except:
                    await ctx.send("Invalid user parameter")
                    return

                db = getDB(db)
                if db == 0:
                    await ctx.send("That database does not exist")
                else:
                    try:
                        cursor = db.cursor()
                        sql = "SELECT subscription FROM members WHERE discordid = %s"
                        val = (ctx.message.mentions[0].id,)
                        cursor.execute(sql, val)
                        result = cursor.fetchall()
                        result = result[0][0]

                        await ctx.send("Subscription expires {}".format(result))
                    except:
                        await ctx.send("User does not exist in database")
            else:
                await ctx.send("You are not authorized to use that command")
        else:
            await ctx.send("Invalid user parameter")


#ADD TIME TO THE SUBSCRIPTION
@bot.command(name = 'addTime', help = "Add a # of days to the user's current subscription time")
async def addTime(ctx, user, db, amount):
    if "-help-" in ctx.message.channel.name or "vision-" in ctx.message.channel.name:
        if checkUserObject(user):
            if checkMod(ctx):
                try:
                    username = ctx.message.mentions[0].name
                    discriminator = ctx.message.mentions[0].discriminator
                    combinedName = username + "#" + discriminator
                    print("addTime({}, {}, {}) used by {}".format(combinedName, db, amount, ctx.author.name))
                except:
                    await ctx.send("Invalid user parameter")
                    return

                db = getDB(db)
                if db == 0:
                    await ctx.send("That database does not exist")
                else:
                    try:
                        cursor = db.cursor()
                        sql = "SELECT subscription FROM members WHERE discordid = %s"
                        val = (ctx.message.mentions[0].id,)
                        cursor.execute(sql, val)
                        result = cursor.fetchall()
                        result = result[0][0]

                        if result.date() < datetime.datetime.today().date():
                            result = datetime.datetime.today()

                        result = result + datetime.timedelta(days=+float(amount))

                        sql = "UPDATE members SET subscription = %s WHERE discord = %s"
                        val = (result, combinedName)
                        cursor.execute(sql, val)
                        member = ctx.message.mentions[0]
                        role = get(member.guild.roles, name="Vision")
                        await member.add_roles(role)
                        await ctx.send("Added {} day(s) to the subscription for {}, new subscription expiry: {}".format(amount, combinedName, result))
                    except:
                        await ctx.send("User does not exist in database")
            else:
                await ctx.send("You are not authorized to use that command")
        else:
            await ctx.send("Invalid user parameter")

#CHECK TIME PLAYED
@bot.command(name = 'played', help = "Check total time the script has been run for the user")
async def played(ctx, user, db):
    if checkUserObject(user):
        try:
            username = ctx.message.mentions[0].name
            discriminator = ctx.message.mentions[0].discriminator
            combinedName = username + "#" + discriminator
            print("played({}, {}) used by {}".format(combinedName, db, ctx.author.name))
        except:
            await ctx.send("Invalid user parameter")
            return

        db = getDB(db)
        if db == 0:
            await ctx.send("That database does not exist")
        else:
            try:
                cursor = db.cursor()
                sql = "SELECT totaltime FROM members WHERE discordid = %s"
                val = (ctx.message.mentions[0].id,)
                cursor.execute(sql, val)
                result = cursor.fetchall()
                result = result[0][0]
                await ctx.send("{} has run the script for {} minutes ".format(combinedName, result))
            except:
                await ctx.send("User does not exist in database")
    else:
        await ctx.send("Invalid user parameter")


#PRINT LEADERBOARD
@bot.command(name = 'leaderboard', help = "Check leaderboard of the top 10 time played for users")
async def leaderboard(ctx, db):
    db = getDB(db)
    if db == 0:
        await ctx.send("That database does not exist")
    else:
        try:
            cursor = db.cursor()
            sql = "SELECT discord FROM members ORDER BY totaltime DESC"
            cursor.execute(sql)
            result = cursor.fetchall()
            for i, user in enumerate(result[:10]):
                userString = str(i).join(user)
                await ctx.send("{}. {}".format(i+1, userString))
        except Exception as e:
            await ctx.send(e)


#ADD A NOTE TO THE USERS ACCOUNT
@bot.command(name = 'addNote', help = "Add a note to the user's account, will overwrite any existing notes")
async def addNote(ctx, user, db, *note):
    if "-help-" in ctx.message.channel.name or "vision-" in ctx.message.channel.name:
        if checkUserObject(user):
            if checkMod(ctx):
                try:
                    username = ctx.message.mentions[0].name
                    discriminator = ctx.message.mentions[0].discriminator
                    combinedName = username + "#" + discriminator
                    print("addNote({}, {}, {}) used by {}".format(combinedName, db, note, ctx.author.name))
                except:
                    await ctx.send("Invalid user parameter")
                    return

                db = getDB(db)
                if db == 0:
                    await ctx.send("That database does not exist")
                else:
                    try:
                        cursor = db.cursor()

                        note = ' '.join(note)

                        sql = "UPDATE members SET notes = %s WHERE discordid = %s"
                        val = (note, ctx.message.mentions[0].id)
                        cursor.execute(sql, val)
                        await ctx.send("Added the note '{}' for {}".format(note, combinedName))
                    except:
                        await ctx.send("A database error has occured")
            else:
                await ctx.send("You are not authorized to use that command")
        else:
            await ctx.send("Invalid user parameter")


@bot.command(name='update', help="Update")
async def update(ctx):
    print("update used by {}".format(ctx.author.name))
    try:
        role = discord.utils.get(ctx.guild.roles, id = 832041017179111424)
        await ctx.send("query started")

        users = role.members

        for user in users:
            await asyncio.sleep(1)
            removeRole = True
            databases = ['2k22', 'mlb21']
            #await ctx.send("Checking {}".format(user))
            for database in databases:
                print("Checking for {} in {}".format(user, database))
                db = getDB(database)
                cursor = db.cursor()
                try:
                    sql = "SELECT subscription FROM members WHERE discordid = %s"
                    val = (user.id,)
                    cursor.execute(sql, val)
                    result = cursor.fetchall()
                except mysql.connector.ProgrammingError:
                    sql = "SELECT discordid FROM members WHERE discordid = %s"
                    val = (user.id,)
                    cursor.execute(sql, val)
                    result = cursor.fetchall()
                    if result:
                        result = [[datetime.datetime.now()],[]]
                if result:
                    result = result[0][0]
                    if result != None:
                        if result.date() >= datetime.datetime.now().date():
                            result = result.date()
                            removeRole = False
                        else:
                            print("Expired Sub: {}".format(result))
                    else:
                        #await ctx.send("Lifetime Sub")
                        removeRole = False
                else:
                    print("No membership")

                if removeRole == False:
                    break

            if removeRole:
                await ctx.send("Removing {} role for {}".format(role.name, user.name))
                await user.remove_roles(role)

    except Exception as e:
        await ctx.send(e)

    await ctx.send("query ended")


#Filter links and other message stuff
bannedDomains = ['free', 'gift', 'nitro']
allowedRoles = ['Admin', 'Moderator', 'Vision Support', 'Developer', 'Verified Host']
mentionedUsers = [] #add members to the list to avoid repeat tagging of individuals
@bot.event
async def on_message(message):
    #if starts with link
    allowed = True
    if 'http' in message.content.lower():
        #Check if banned domain
        for domain in bannedDomains:
            if domain in message.content.lower():
                allowed = False
        for role in message.author.roles:
            if role.name in allowedRoles:
                allowed = True
        if not allowed:
            await message.delete()
            print(str(message.content) + " sent by " + str(message.author.name) + " deleted")
        else:
            await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    #Messages in general chat channel
    if 'general-chat' in message.channel.name:
        if message.author.name == 'dricon':
            await message.add_reaction('🐐')
        if len(message.author.roles) <= 1 and not message.author.bot and message.author.name not in mentionedUsers:
            await message.channel.send("{} you do not yet have a member role, visit <#794784947566280744> to verify and gain access to the rest of the discord".format(message.author.mention))
            mentionedUsers.append(message.author.name)
    #random responses from the bot
    if 'bye' in message.content.lower():
        if not message.author.bot:
            await message.channel.send("Bye {} !".format(message.author.mention))
    elif '<@!863956599738597416>' in message.content:
        print(message.content)
        await message.channel.send("I'm just a bot")
        mentionedUsers.append(message.author.name)

    #Someone requests their ID
    if 'my id' in message.content.lower() or 'my code' in message.content.lower() or 'my user id' in message.content.lower():
        await message.channel.send("Hey {},\nIf you forgot your ID, type .getID \nIf your ID is giving a failed verification because you changed devices, type .reset".format(message.author.mention))

    if 'error code ' in message.content.lower():
        await message.channel.send("Error codes don't mean anything. Read the error.")

    await bot.process_commands(message)


bot.run(TOKEN)
