import datetime
# exportação biblioteca/framework discord
import discord
from discord.ext import commands, tasks



# deixar as intenção de mensagem padrão
intents = discord.Intents.default()
intents.messages = True # Habilita a intenção de mensagens para receber eventos de mensagem
intents.message_content = True # Habilita a intenção de conteúdo de mensagem


bot = commands.Bot(command_prefix="!", intents=intents)
# fazer o prefix e dar as intenções para o bot
