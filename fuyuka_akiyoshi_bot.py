import math
import dadosBot
import inicialConfig
import requests
import asyncio


@inicialConfig.bot.event
# essa função iniciará o bot
async def on_ready():
    print(f'{inicialConfig.bot.user} está conectado!')
    # current_time.start()


@inicialConfig.bot.event
async def on_message(message):
    if message.author == inicialConfig.bot.user:
    # verifica se a mensagem foi mandada pelo bot
    # para evitar loop infinitos
        return
    
    msg = str(message.content).lower().split()

    for p in msg:
        if p in dadosBot.palavrões:
            await message.channel.send(
                f'Por favor, {message.author.name}, não ofenda os demais usuários.'
            )
            await message.delete()

    await inicialConfig.bot.process_commands(message)


bot_context = dadosBot.BotContext()

@inicialConfig.bot.command(name='/code')
async def my_command(ctx):
    if ctx.author == inicialConfig.bot.user:
        return
    await ctx.send(
        '```Digite abaixo o código:```'
    )


    @inicialConfig.bot.event
    async def on_message(message):
        await bot_context.process_message(message)


@inicialConfig.tasks.loop(seconds=5)
async def current_time():
    now = inicialConfig.datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for guild in inicialConfig.bot.guilds:
        if guild.name in dadosBot.server_channel_mapping:
            channel_id = dadosBot.server_channel_mapping[guild.name]
            channel = inicialConfig.bot.get_channel(channel_id)
            if channel:
                await channel.send('Data atual: ' + now)
                print(f"Enviado para o canal no servidor '{guild.name}'.")
                break


@inicialConfig.bot.command(name='calculate')
async def python_interpreter(ctx, *expression):
    format_expression = ''.join(expression)
    result = eval(format_expression)
    await ctx.send(f'>>> {str(result)}')




# @inicialConfig.bot.command(name='verificar')
# async def python_interpreter(ctx):
#     if platform == 'win32':
#         await ctx.send('Sistema Operacional: Windows')
#     elif platform == 'linux':
#         await ctx.send('Sistema Operacional: Linux')
#     else:
#         await ctx.send('Um Sistemas Operacional diferente de Windows e Linux')




# estudar ponteiros 
@inicialConfig.bot.command(name='formPascal')
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




@inicialConfig.bot.command()
async def binance(ctx, coin, base):
    
    try:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}')

        data = response.json()
        price = float(data.get('price'))

        if price:
            await ctx.send(f'O valor do par {coin}/{base} é {dadosBot.formatação(price)}')
        else:
            await ctx.send(f'O valor do par {coin}/{base} é inválido ou incorreto!')
    except Exception as e:
        await ctx.send(f'<{e}> Tente Novamente!')


@inicialConfig.tasks.loop(seconds=10)
async def current_time_varia_bitcoin():

    try:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')

        data = response.json()
        price = float(data.get('price'))

        for guild in inicialConfig.bot.guilds:
            if guild.name in dadosBot.server_channel_mapping:
                channel_id = dadosBot.server_channel_mapping[guild.name]
                channel = inicialConfig.bot.get_channel(channel_id)
                if channel:
                    if price:
                        formatted_price = dadosBot.formatação(price)
                        dadosBot.pilha.append(formatted_price)
                        await channel.send(f'Preço atual do Bitcoin: ${formatted_price}')
                        print(f"Enviado para o canal no servidor '{guild.name}'.")
                    break
    except Exception as e:
        await channel.send(f'<{e}> Tente Novamente!')


@inicialConfig.bot.command(name='variaçãoBitcoin')
async def varia_bitcoin_control(ctx, command_user):

    try:
        str(command_user).lower()
        if command_user == 'start':
            current_time_varia_bitcoin.start()
        
        elif command_user == 'stop':
            current_time_varia_bitcoin.stop()
            await asyncio.sleep(10)
            dadosBot.states_BTC_price.append(dadosBot.pilha[0])
            dadosBot.states_BTC_price.append(dadosBot.pilha[-1])
            # bot_context.bot_state.parar = True
            if dadosBot.states_BTC_price:
                await ctx.send(f">>> Primeiro Preço: {dadosBot.states_BTC_price[0]}\nUltimo preço: {dadosBot.states_BTC_price[-1]}")
            else:
                await ctx.send("Nenhum preço de Bitcoin armazenado ainda.")
        else:
            await ctx.send('>>> Command not invalid')            
        dadosBot.states_BTC_price.clear()
        dadosBot.pilha.clear()
    except Exception as e:
        await ctx.send(f'<{e}> Tente Novamente!')


# o método run usara o token do bot como parâmetro
inicialConfig.bot.run('MTIxODk4NzMwNjYzMjA4OTcwMg.Gku2JU.tthyfwBHdcXQxGmrJUhWgoIhU-75x4BFRRAwIk')
