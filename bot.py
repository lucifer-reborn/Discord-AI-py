import discord, json, openai
from discord.ext import commands

with open("config.json") as f:
    cfg = json.load(f)

openai.api_key = cfg["api_key"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=cfg["prefix"], intents=intents)

data = {"ai_channel": None}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def setaichannel(ctx, channel: discord.TextChannel):
    data["ai_channel"] = channel.id
    await ctx.reply(f"AI channel set to {channel.mention}")

@bot.command()
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.reply("🔒 Channel locked.")

@bot.command()
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.reply("🔓 Channel unlocked.")

@bot.command()
async def ai(ctx, *, msg):
    if data["ai_channel"] and ctx.channel.id != data["ai_channel"]:
        return await ctx.reply("Use AI in the set channel.")
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":msg}],
            max_tokens=100
        )
        await ctx.reply(res.choices[0].message.content)
    except Exception as e:
        await ctx.reply(f"Error: {e}")

bot.run(cfg["token"])
