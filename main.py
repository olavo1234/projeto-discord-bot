# -*- coding: utf-8 -*-
import math
import botStatus
import initialSettings
import requests
import asyncio
import botData
from sys import platform
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound




@initialSettings.bot.event
# essa função iniciará o bot
async def on_ready():
    print(f'{initialSettings.bot.user} está conectado!')
    # esse método está desativado faz parte do current_time 
    # current_time.start()


@initialSettings.bot.event
async def on_command_error(ctx, error):
    # Esse evento será chamado caso tenha exeções
    if isinstance(error, MissingRequiredArgument):
        # Em caso de exeções de argumentos
        await ctx.send('Favor enviar todos os Argumentos, mais duvidas comsulte "!?help"')
    elif isinstance(error, CommandNotFound):
        # Em caso de comando não encontrado
        await ctx.send('O comando não existe, mais duvidas comsulte "!?help"')
    else:
        # Ele avisa o erro
        raise error


@initialSettings.bot.event
async def on_message(message):
    if message.author == initialSettings.bot.user:
    # verifica se a mensagem foi mandada pelo bot
    # para evitar loop infinitos
        return
    
    msg = str(message.content).lower().split()
    # ".split()" vai dividir essa frase em um array de palavras 
    for p in msg:
        if p in botData.palavrões:
            # E procurar essas palavras no banco de dados atrás de palavões
            await message.channel.send(
                f'Por favor, {message.author.name}, não ofenda os demais usuários.'
            )
            # E irá deletar essa mensagem que inflinge a regra de palavrões
            await message.delete()
    # Nesse código o bot espera prosessar todos so comandos 
    await initialSettings.bot.process_commands(message)


bot_context = botStatus.BotContext()
# Criar Objeto para gerenciar o status do bot

@initialSettings.bot.command(name='/code', help="Irá formatar um texto da caixa normal em código")
async def my_command(ctx):
    if ctx.author == initialSettings.bot.user:
        # Vai verificar para ver se as mensagens não são do próprio bot
        return
    await ctx.send(
        '```Digite abaixo o código:```'
        # Pede um input do Usuário 
    )

    # Dentro desse evento tem um segundo evento 
    # que irá chamar meu Objeto e mandar a mensagem para o sistema de gerenciamento
    # no botStatus.py na classe RodadaManager
    @initialSettings.bot.event
    async def on_message(message):
        await bot_context.process_message(message)


# Desativado

# @initialSettings.tasks.loop(seconds=5)
# async def current_time():
#     now = initialSettings.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     for guild in initialSettings.bot.guilds:
#         if guild.name in botData.server_channel_mapping:
#             channel_id = botData.server_channel_mapping[guild.name]
#             channel = initialSettings.bot.get_channel(channel_id)
#             if channel:
#                 await channel.send('Data atual: ' + now)
#                 print(f"Enviado para o canal no servidor '{guild.name}'.")
#                 break


@initialSettings.bot.command(name='calculate', help="Vai usar o ambiente python para gerar resultados matemáticos")
async def python_interpreter(ctx, *expression):
    # O usuário vai digitar código python para realizar calculos
    format_expression = ''.join(expression)
    # para formar uma expressão se tira todos os espaços
    result = eval(format_expression)
    # se utiliza o "eval" para converter a string em código 
    await ctx.send(f'>>> {str(result)}')



@initialSettings.bot.command(name='verificarLocalBot', help="Verificar o OS local de onde o código é rodado")
async def verificar_os(ctx):
    
    windows = 'wind32'
    linux = 'linux'
    
    if platform == windows:
        await ctx.send('O Usuário está no Sistema Operacional: Windows')
    elif platform == linux:
        await ctx.send('O Usuário está no Sistema Operacional: Linux')
    else:
        await ctx.send('O Usuário está em um Sistemas Operacional diferente de Windows e Linux')



# muito complicado para mim
# estudar ponteiros 
@initialSettings.bot.command(name='formPascal', help="Formar um triângulo pascal pela sua base")
async def pascalTriangle(ctx, num: int):

    def combination(n, k):
        # Cálculo iterativo de combinação
        result = 1
        for r in range(min(k, n - k)):
            result = result * (n - r) // (r + 1)
        return result

    async def pascals_triangle(rows):
        for row in range(rows):
            answer = ""

            for column in range(row + 1):
                answer += str(combination(row, column)) + " "

            await ctx.send(answer)
    
    await pascals_triangle(num)




@initialSettings.bot.command(help="Mostrar a relação de uma criptomoeda pela base, Coin/Base")
async def binance(ctx, coin, base):
    # try para tentar e estabilizar o bot quando a API não funcionar
    try:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}')
        # Se utiliza o API da binance para pegar dados de criptomoedas
        botData = response.json()
        # Chamar todos so dados da API em um json
        price = float(botData.get('price'))
        # E pegar o preço formatando em float para a formatação

        # utilizamos a função de formatação para BRL
        if price:
            await ctx.send(f'O valor do par {coin}/{base} é {botStatus.formatação(price)}')
        else:
            await ctx.send(f'O valor do par {coin}/{base} é inválido ou incorreto!')
    except Exception as e:
        await ctx.send(f'<{e}> Tente Novamente!')


@initialSettings.tasks.loop(seconds=10)
# Será iniciado um loop pela task do discord
async def current_time_varia_btc():

    try:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')

        data = response.json()
        price = float(data.get('price'))

        for guild in initialSettings.bot.guilds:
            # Na parte do desenvolvimento servidores são chamados de guilds
            # Nesse caso o loop vai passar por cada servidor onde o bot está e so parará
            # Quando encontrar um servidor dentro de um dicionário no banco de dados
            if guild.name in botData.server_channel_mapping:
                channel_id = botData.server_channel_mapping[guild.name]
                channel = initialSettings.bot.get_channel(channel_id)
                # Se pega o cannal pelo id 
                if channel:
                    if price:
                        formatted_price = botStatus.formatação(price)
                        botStatus.pilha.append(formatted_price)
                        # E utilizamos o send normalmente depois do "get_channel()" 
                        await channel.send(f'Preço atual do Bitcoin: ${formatted_price}')
                        print(f"Enviado para o canal no servidor '{guild.name}'.")
                    break
    except Exception as e:
        await channel.send(f'<{e}> Tente Novamente!')


@initialSettings.bot.command(name='variaçãoBitcoin', help="monstra a variação do Bitcoin")
async def varia_bitcoin_control(ctx, command_user):
    # Esse bloco de código faz parte do "current_time_varia_btc()"
    try:
        str(command_user).lower()
        if command_user == 'start':
            # O usuário terá que digitar comandos de start e stop
            current_time_varia_btc.start()
            # Isso fará a task de loop parar
        
        elif command_user == 'stop':
            current_time_varia_btc.stop()
            # Quando parar vamos esperar um tempo de 10 segundos para enviar todos os dados
            await asyncio.sleep(10)
            # Iremos adicionar todos as variações para uma pilha 
            botStatus.states_BTC_price.append(botStatus.pilha[0])
            # E enviaremos o primeiro e último preço da sequência da pilha para o array "states_BTC_price" 
            botStatus.states_BTC_price.append(botStatus.pilha[-1])
            if botStatus.states_BTC_price:
                # Isso irá exibir essas informções do 
                await ctx.send(f">>> Primeiro Preço: {botStatus.states_BTC_price[0]}\nUltimo preço: {botStatus.states_BTC_price[-1]}")
            else:
                await ctx.send("Nenhum preço de Bitcoin armazenado ainda.")
        else:
            await ctx.send('>>> Command not invalid')
        # No final limpamos a pilha e o array para não ter lixo na proxima ativação  
        botStatus.states_BTC_price.clear()
        botStatus.pilha.clear()
    except Exception as e:
        await ctx.send(f'<{e}> Tente Novamente!')


@initialSettings.bot.command(name='segredo', help="Emvia uma mensagem no privado")
async def secret(ctx):
    try:
        await ctx.author.send('200pp vem nunca??')
    except initialSettings.discord.errors.Forbidden:
        # A exeção forbidden ocorre quando o usuário desativo as mensagens diretas
        # nesse cado enviaremos um aviso para ativar
        await ctx.send(
            'Por favor ative as mensagens diretas dos membros do servidor em:'
            '\nConfiguraçães de Usuários > Privacidade e segurança >' 
            ' Permitir mensagens diretas de membros do servidor'
        )


@initialSettings.bot.event
async def on_reaction_add(reaction, user):
    # Pegar os id do cargo e salvar em uma variavel
    role_happy = user.guild.get_role(1236433934515044382)
    role_bad = user.guild.get_role(1236434116140990654)

    if reaction.emoji == '👍':
        # Add e remove para adicionar esse cargo
        await user.add_roles(role_happy)
        await user.remove_roles(role_bad)
    elif reaction.emoji == '💩':
        await user.add_roles(role_bad)
        await user.remove_roles(role_happy)


@initialSettings.bot.command(name='image', help="irá emviar embed com imagens aleatórias")
async def get_random_image(ctx):
    # o embed é uma caixa de mensagem do discord onde tem titulo, descrição, imagens e fields 
    url_image = "https://picsum.photos/1920/1080" 
    # Nesse caso para a imagens será usado o API de imagens aleatórias
    
    embed_image = initialSettings.discord.Embed(
        title="Resultado da busca da imagem",
        description="Essa busca é totalmente aleatória",
        color=0x0000ff
    )

    embed_image.set_author(
        name=initialSettings.bot.user.name,
        icon_url=initialSettings.bot.user.avatar
    )

    embed_image.set_footer(
        text="Feito por " + initialSettings.bot.user.name,
        icon_url=initialSettings.bot.user.avatar
    )

    embed_image.set_image(url=url_image)

    embed_image.add_field(
        name="API", 
        value="API usada: https://picsum.photos"
    )

    embed_image.add_field(
        name="Parâmetros",
        value="{largura}/{altura}"
    )

    embed_image.add_field(
        name="Exemplo: ",
        value=url_image,
        inline=False
    )

#   nesse caso o "send()" terá um argumento próprio para embed
    await ctx.send(embed=embed_image)


@initialSettings.bot.command(name="nameDev", help="Vai pegar o nome do desenvolvedor")
async def get_name_dev(ctx):
    # Essa função assincrona so irá pegar meu nome de usuário do discord e avatar
    dev = await initialSettings.bot.fetch_user(botData.ID_USER)
    # Se usa "fetch_user()" para user que não estiver no histórico
    if dev is not None:
        await ctx.send(dev.name)
        await ctx.send(dev.avatar)
    else:
        print('Usuário não encontrado')


@initialSettings.bot.command(name="?help", help="Um guia mais detalhado dos comandos")
async def help(ctx):

    embed_help_message = initialSettings.discord.Embed(
        title='O comando "!?help" irá ajudar com um guia abaixo.',
        description="O Fuyuka Akiyoshi Bot foi criado com o intuito de estudo,"
        " todos os comando são testes para ver o comportamento do bot.",
        color=0xadd8e6
    )

    dev = await initialSettings.bot.fetch_user(botData.ID_USER)
    
    embed_help_message.set_footer(
        text="Feito por " + dev.name,
        icon_url=dev.avatar
    )

    embed_help_message.add_field(
        name="Comando: /code", 
        value=
            "O comando é usado para formatar o código do campo de texto nornal,"
            " se escreve '!/code' e o bot pedirá a baixo o seu código."
    )

    embed_help_message.add_field(
        name="Comando: binance",
        value="O Comando servirá para ver o valor de um criptmoeda comparado com uma moeda,"
        " se escreve '!binance' e junto os parâmetros: Coin/Base."
    )


    embed_help_message.add_field(
        name="Comando: calculate",
        value="O Comando servirá para calcular um valor sequindo a biblioteca math e os códigos nativos do python,"
        " se escreve '!calculate ' e os parâmetros communs são +, -, *, /, //, **. Para mais informaçãoes do math: https://docs.python.org/3/library/math.html"
    )

    embed_help_message.add_field(
        name="Comando: formPascal", 
        value=
            "O comando é usado para formar um triângulo de Pascal,"
            " se escreve '!formPascal' junto com a base como parâmetro para mais"
            "informaçãoes: https://jwilson.coe.uga.edu/EMAT6680Su12/Berryman/6690/BerrymanK-Pascals/BerrymanK-Pascals.html"
    )

    embed_help_message.add_field(
        name="Comando: help", 
        value=
            "Além do comando '!?help' que é mais completo o '!help' é uma versão padrão que irá mostrar mensagens simples"
    )

    embed_help_message.add_field(
        name="Comando: image", 
        value=
            "O comando '!image' irá exibir em uma embed imagens aleatórias."
    )

    embed_help_message.add_field(
        name="Comando: nameDev", 
        value=
            "O comando '!nameDev' irá exibir em o nome e o avatar do desenvolvedor do bot."
    )

    embed_help_message.add_field(
        name="Comando: segredo", 
        value=
            "O comando '!segredo 'enviará um mensagem no privado de quem utilizar o comando."
    )

    embed_help_message.add_field(
        name="Comando: variaçãoBitcoin", 
        value=
            "O comando '!variaçãoBitcoin' irá utilizar ficar verificando o preço Bitcoin, e irá ficar retornado em um loop esses valores."
            "Além disso terá o '!variaçãoBitcoin start' para começar o loop e '!variaçãoBitcoin stop' para parar o loop, e no final"
            "irá exibir o peço inicial da bitcoin e o preço final após a parada."
    )

    embed_help_message.add_field(
        name="Comando: verificarLocalBot", 
        value=
            "O comando '!verificarLocalBot' enviará um mensagem mostrando o Sistema Operacional local de onde o código do bot está sendo rodado. "
    )

    await ctx.send(embed=embed_help_message)


# o método run usara o token do bot como parâmetro
initialSettings.bot.run(initialSettings.TOKEN_bot_env)
