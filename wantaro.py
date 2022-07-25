import discord, asyncio, re, os
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot
from jamdict import Jamdict


intents=discord.Intents.all()
jam = Jamdict()
# using Jamdict(memory_mode=True) loads entire database into Wantaro
# also makes the first lookup slow, so make a test lookup before event handler

load_dotenv('data\ids.env')
TOKEN = os.getenv('DISCORD_TOKEN')
jsaGenChat = int(os.getenv('JSAGENCHAT'))
testGrounds = int(os.getenv('TESTGROUNDS'))
testServer = int(os.getenv('TESTSERVER'))
jsaServer = int(os.getenv('JSASERVER'))
jsaMember = int(os.getenv('JSAMEMBER'))
gaming = int(os.getenv('GAMING'))
jpmedia = int(os.getenv('JPMEDIA'))
study = int(os.getenv('STUDY'))
cooking = int(os.getenv('COOKING'))

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')

blacklist = [583450025548316692]
bad_words = []
badWords = open(r'data\bad words.txt', 'r', encoding='utf-8')
for word in badWords.readlines():
    bad_words.append(word.strip())
print(bad_words)
badWords.close()
# event handler
#########################################################################################################
@client.event
async def on_ready():
    print('Wantaro Online!')


@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    elif re.search('wantaro', message.content.lower()):
        await message.add_reaction('<:wantaroemoji:945508920212992010>')

    # prevents on_message from skipping command calls
    await client.process_commands(message) 

@client.event
async def on_member_join(member):
    channel = client.get_channel(testGrounds)
    role = (client.get_guild(jsaServer)).get_role(jsaMember)
    await member.add_roles(role) 
    print(f'{member.mention} has joined the server.')
    await channel.send(f'JSAへようこそ、{member.mention}！')

# error handler 
@client.event
async def on_command_error(ctx, error):
    errorF = open("data\errorlog.txt", 'a+', encoding='utf8')
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        errorF.write(f'{ctx.author} entered no args into [{ctx.command}]\n')
        errorF.write(f'User input: {ctx.message.content}\n\n')
        errorF.close()
        print(error)
        await ctx.send('No argument entered...')

    elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        errorF.write(f'Invoke error from [{ctx.command}]: ' + str(error) + '\n')
        errorF.write(f'User input: {ctx.message.content}\n\n')
        print(error)
        errorF.close()

    else:
        errorF.write(f'Unknown error from [{ctx.command}]: ' + str(error) + '\n')
        errorF.write(f'User input: {ctx.message.content}\n\n')
        print(error)
        errorF.close()

# command handler 
#######################################################################################################
@client.command()
async def lookup(ctx, arg): # first letter has to be capitalized if its a proper noun
    if (arg in bad_words):
        await ctx.message.add_reaction('🤨')
    result = jam.lookup(arg, True) # send a message about this if arg is in English 
    string = ""
    if(len(result.entries) != 0):
        for item in result.entries:
            string += item.text(no_id=True) + '\n'
        await ctx.send(string)

    elif(len(result.chars) != 0):
        for item in result.chars:
            string += item.text(no_id=True) + '\n'
        await ctx.send(string)

    else:
        for item in result.names:
            string += item.text(no_id=True) + '\n'
        await ctx.send(string)

@client.command()
async def ping(ctx):
    await ctx.send('ワンワン！')
    await ctx.send(str(client.latency) + ' ms')

@client.command()
async def wantaro(ctx):
    await ctx.send('ワンワン！')

@client.command()
async def game(ctx):
    await ctx.send('is u issy ? 💀 ')

@client.command()
async def meeting(ctx):
    await ctx.send("ワンワン！\n"
                   "Meetings start at 6pm every Friday\n"
                   "会議は毎週の金曜日の午後6時に開始します\n"
                   f'{ctx.author.mention}')

@client.command()
async def help(ctx):
    commandList = []
    embed = discord.Embed()
    for item in client.commands:
        commandList.append(item.name)
    commandList.sort()
    file = open("data\commands.txt", encoding='utf-8')
    for command in commandList:
        line = file.readline()
        embed.add_field(name=command,value=line)
    file.close()
    await ctx.author.send(embed=embed)
    


@client.command()
async def iam(ctx, arg):
    roleDict = {
        "gaming": gaming,
        "jpmedia": jpmedia,
        "study": study,
        "cooking": cooking
    }

    if(arg in roleDict):
        role = (client.get_guild(jsaServer)).get_role(roleDict[arg])
        print(role)
        await member.add_roles(role)
        await ctx.message.delete()

    
@client.command()
async def suggestion(ctx):
    suss = open("data\suggestions.txt", 'a+', encoding='utf-8')
    suss.write(f'{ctx.message.author}: {ctx.message.content}\n\n')
    suss.close()
    await ctx.message.delete()
    await ctx.send('ワンワン！\n'
                   '説得してみる！', delete_after=5)



file = open("data\commands.txt", encoding='utf-8')
errorF = open("data\errorlog.txt", 'a+')
check1 = len(file.readlines())
check2 = len(client.commands)
if(check1 != check2):
    print('check')
    errorF.write('Not all commands are defined in commands.txt.\n\n')
    file.close()
    errorF.close()
    exit()
        
client.run(TOKEN)
