# squatsbot.py

import os
from os.path import exists

import discord
from discord.ext import tasks, commands

import csv

import datetime

TOKEN = "" #secret, do not share!

notificationDelay = 24 #in hours

class CustomClient(discord.Client):

    #///////////////////////////////////////////////////////////////////////////////////
    #   Method Run On Bot Connection To Discord Servers
    async def on_ready(self):
        today = datetime.date.today()
        now = datetime.datetime.now()
        startTime = now.strftime("%H:%M:%S")
        print("Today's date:", today)
        print("Start Time : ", startTime)
        # dates = list()
        # dates.append(today.isoformat())
        # for i in range(30):
        #     dates.append((today + datetime.timedelta(i)).isoformat())
        # print (dates)
        print(str(client.user) + ' has connected to Discord!')
        for guild in client.guilds:
            print('Connected to ... ' + str(guild)+'!')
            if(exists(str(guild) +'.csv')):
                print('    '+str(guild)+'.csv found!')
                print('    ...Ready!')
            else:
                print('    '+str(guild)+'.csv MISSING! Creating...')
                with open (str(guild)+'.csv', 'w') as csvIn: #will associating the guild name with file storage be a problem? What if server is renamed ... fix it later?
                    filewriter = csv.writer(csvIn)
                    filewriter.writerow(['Server', str(guild)])
                    filewriter.writerow(['Date', '2021-12-15', '2021-12-16', '2021-12-17', '2021-12-18', '2021-12-19', '2021-12-20', '2021-12-21', '2021-12-22', '2021-12-23', '2021-12-24', '2021-12-25', '2021-12-26', '2021-12-27', '2021-12-28', '2021-12-29', '2021-12-30', '2021-12-31', '2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05', '2022-01-06', '2022-01-07', '2022-01-08', '2022-01-09', '2022-01-10', '2022-01-11', '2022-01-12', '2022-01-13', '2022-01-14'])
                    filewriter.writerow(['Standard',10,15,20,25,0,30,35,40,45,0,50,55,60,65,0,70,75,80,85,0,90,95,100,105,0,110,115,120,125,130])
                    filewriter.writerow(['Hard',50,55,60,0,70,75,80,0,100,105,110,0,130,135,140,0,150,155,160,0,180,185,190,0,220,225,230,0,240,250])
                    filewriter.writerow(['USERS'])
                print('    ...Done. Ready!')

    #///////////////////////////////////////////////////////////////////////////////////
    #   Messaging new members to discord to get swole!
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send('Hi '+ member.name +', welcome to the discord! If you want to get swole hit me up fam.')

    #///////////////////////////////////////////////////////////////////////////////////
    #   method run anytime a message is dropped in a channel visible to the bot
    async def on_message(self, message):
        #dont respond to self
        if message.author == client.user:
            return
        
        #///////////////////////////////////////////////////////////////////////////////////
        #   Help text/ explainer
        if message.content == '!SquatsBot Help':
            response = "Looks like you want to get swole... **BEHOLD THY COMMANDS!**\n----------------------------------------------------------------------------\n!SquatsBot Swoletime - Sign up for daily Squatifications!\n!SquatsBot Swolechief Managed - End your daily Squatifications.\n!SquatsBot Start - Start bot notifications! The time at which this command is sent will be the time participants will get a reminder each day!\n----------------------------------------------------------------------------\nPS: Async discord tasks are new to me, so I have no idea how to shut them off yet. Don't start the challenge more than once.\nIf you need terminate functionality tell me and I'll just kill the script host. - Tesnich"
            #\n!SquatsBot Heathens - Show active squatters! *Maybe lock the door next time...*
            await message.channel.send(response)

        #///////////////////////////////////////////////////////////////////////////////////
        #   Subcribe to notifications
        if message.content == '!SquatsBot Swoletime':
            guildFileName = str(message.guild) +'.csv' #depending on  when server is added file might not exist
            userFound = False
            lines = list()
            users = list()

            with open (guildFileName, 'r') as csvOut:
                fileReader = csv.reader(csvOut)
                for row in fileReader:
                    if(row[0] == 'USERS'):
                        for item in row:
                            users.append(item)
                            if (item == str(message.author.id)):
                                userFound = True
                    else:
                        lines.append(row)

            if (userFound):
                response = "**Chillout" + str(message.author) + ",** you are already a squatter."
                await message.channel.send(response)
            else:
                with open (guildFileName, 'w') as csvIn:
                    fileWriter = csv.writer(csvIn)
                    for line in lines:
                        fileWriter.writerow(line)
                    users.append(str(message.author.id))
                    fileWriter.writerow(users)

                response = "**Your journey has begun " + str(message.author) + "!** You will get a daily reminder to participate for the duration of the event!"
                await message.channel.send(response)
        
        #///////////////////////////////////////////////////////////////////////////////////
        #   Un-subcribe from notifications
        if message.content == '!SquatsBot Swolechief Managed':
            guildFileName = str(message.guild) + '.csv' #depending on  when server is added file might not exist
            userFound = False
            lines = list()
            users = list()

            with open (guildFileName, 'r') as csvOut:
                fileReader = csv.reader(csvOut)
                for row in fileReader:
                    if(row[0] == 'USERS'):
                        for item in row:
                            if (item != str(message.author.id)):
                                users.append(item)
                            else:
                                userFound = True
                    else:
                        lines.append(row)
                lines.append(users)

            if (userFound):   
                with open (guildFileName, 'w') as csvIn:
                    fileWriter = csv.writer(csvIn)
                    for line in lines:
                        fileWriter.writerow(line)

                response = "**Congrats on getting swole " + str(message.author) + "!** Go out there and show off those beautiful leg muscles! Kick in a door or something idk."
                await message.channel.send(response)
            else:
                response = "**You are not currently subscribed to squatifications, " + str(message.author) + ".** Nothing has been done."
                await message.channel.send(response)
        
        #///////////////////////////////////////////////////////////////////////////////////
        #   Get an update on progress of event
        # if message.content == '!SquatsBot Update':
        #     response = "Update!"
        #     await message.channel.send(response)

        #///////////////////////////////////////////////////////////////////////////////////
        #   See all subcribed participants
        # if message.content == '!SquatsBot Heathens':
        #     response = "We got lots of people, james is just busy and hasn't coded this yet."
        #     await message.channel.send(response)

        #///////////////////////////////////////////////////////////////////////////////////
        #   Comand to start event notifications
        if '!SquatsBot Start' in message.content:
            if (message.author.top_role.permissions.administrator or str(message.author.id) == '234466321465737216'):
                response = "30 Day Challenge Started! Participants will be at notified every " + str(notificationDelay) + " hours."
                await message.channel.send(response)
                client.MentionUsers.start(message)
            else:
                response = "You must be an admin to use this command :("
                await message.channel.send(response)

    #///////////////////////////////////////////////////////////////////////////////////
    #   Looping task to mention all subscribed users in a daily reminder
    @tasks.loop(hours=notificationDelay)
    async def MentionUsers(self, message):
        now = datetime.datetime.now()
        print("Mention Users Started ... ", now.strftime("%H:%M:%S"))

        today = datetime.date.today().isoformat()
        day = 0
        standardSquats = 8888
        hardSquats = 9999

        guildFileName = str(message.guild) +'.csv'
        userNames = ""

        with open (guildFileName, 'r') as csvOut:
                fileReader = csv.reader(csvOut)
                for row in fileReader:
                    if(row[0] == 'Date'):
                        for item in row:
                            if item == today:
                                break
                            else:
                                day += 1
                    if(row[0] == 'Standard'):
                        standardSquats = row[day]
                    if(row[0] == 'Hard'):
                        hardSquats = row[day]
                    if(row[0] == 'USERS'):
                        for item in row:
                            if item == 'USERS':
                                continue
                            else:
                                userNames += '<@' + item + '> ' 

        await message.channel.send(userNames + 'Welcome to day ' + str(day) + ' of squats! Complete **' + str(standardSquats) + '** squats for the standard challenge, or **'+ str(hardSquats)+ '** for the advanced. Good Luck!')
        

client = CustomClient()
client.run(TOKEN)