# -*- coding: utf-8 -*-
import os
import datetime
# exportação biblioteca/framework discord
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv




# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Variável de ambiente do token do bot local no meu pc
# TOKEN_bot_local = os.getenv('token_bot_local')

# token utilizando o .env
TOKEN_bot_env = os.getenv('TOKEN_BOT_env')


# deixar as intenção de mensagem padrão
intents = discord.Intents.default()
intents.messages = True # Habilita a intenção de mensagens para receber eventos de mensagem
intents.message_content = True # Habilita a intenção de conteúdo de mensagem


bot = commands.Bot(command_prefix="!", intents=intents)
# fazer o prefix e dar as intenções para o bot
