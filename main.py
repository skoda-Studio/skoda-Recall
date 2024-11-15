import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from art import text2art  
from colorama import Fore, Style, init
import random

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        ascii_art_text = text2art("Skoda Studio")
        print(Fore.LIGHTCYAN_EX + ascii_art_text + Style.RESET_ALL)
        print(Fore.LIGHTGREEN_EX + f"Logged in as {bot.user}" + Style.RESET_ALL)
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="Skoda®Studio"))
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"Error in on_ready event: {e}" + Style.RESET_ALL)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    role = discord.utils.get(message.guild.roles, id=ROLE_ID)
    if role not in message.author.roles:
        return

    if message.author in message.mentions:
        await message.channel.send(f"{message.author.mention} لا يمكنك نداء نفسك")
        return

    if len(message.mentions) > 0:
        if len(message.content.strip()) == len(message.mentions[0].mention):
            mentioned_user = message.mentions[0]
            caller_mention = message.author.mention
            jump_url = message.jump_url

            message_choices = [
                f"تم طلبك في روم : {jump_url} \n الشخص الذي استدعاك: {caller_mention}",
                f"تم ذكرك في روم : {jump_url} \n من قبل: {caller_mention}"
            ]
            selected_message = random.choice(message_choices)

            try:
                await mentioned_user.send(selected_message)
                await message.channel.send(f"تم مناداته بنجاح \n {mentioned_user.mention}")
            except discord.Forbidden:
                await message.channel.send(f"{caller_mention} \n قام بمحاولة مناداتك ولكن تم رفض الرسالة الخاصة بسبب إعدادات الخصوصية الخاصة بك. \n {mentioned_user.mention}")
            except discord.HTTPException as e:
                await message.channel.send(f"حدث خطأ أثناء محاولة مناداتك، يرجى المحاولة لاحقًا. {mentioned_user.mention}")

    await bot.process_commands(message)

bot.run(TOKEN)
