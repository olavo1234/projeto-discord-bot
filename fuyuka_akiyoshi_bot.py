import math
import dadosBot
import inicialConfig
import requests
import asyncio
from sys import platform



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



@inicialConfig.bot.command(name='verificarLocalBot')
async def verificar_os(ctx):
    
    windows = 'wind32'
    linux = 'linux'
    
    if platform == windows:
        await ctx.send('O Usuário está no Sistema Operacional: Windows')
    elif platform == linux:
        await ctx.send('O Usuário está no Sistema Operacional: Linux')
    else:
        await ctx.send('O Usuário está em um Sistemas Operacional diferente de Windows e Linux')



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


@inicialConfig.bot.command(name='segredo')
async def secret(ctx):
    try:
        await ctx.author.send('200pp vem nunca??')
    except inicialConfig.discord.errors.Forbidden:
        await ctx.send(
            'Por favor ative as mensagens diretas dos membros do servidor em:'
            '\nConfiguraçães de Usuários > Privacidade e segurança >' 
            ' Permitir mensagens diretas de membros do servidor'
        )


@inicialConfig.bot.event
async def on_reaction_add(reaction, user):
    # pegar os id do cargo e salvar em uma variavel
    role_happy = user.guild.get_role(1236336602221903882)
    role_bad = user.guild.get_role(1236336701224259655)

    if reaction.emoji == '👍':
        # add e remove para adicionar esse cargo
        await user.add_roles(role_happy)
        await user.remove_roles(role_bad)
    elif reaction.emoji == '💩':
        await user.add_roles(role_bad)
        await user.remove_roles(role_happy)


@inicialConfig.bot.command(name='image')
async def get_random_image(ctx):
    url_image = "https://picsum.photos/1920/1080" 
    
    embed_image = inicialConfig.discord.Embed(
        title="Resultado da busca da imagem",
        description="Essa busca é totalmente aleatória",
        color=0x0000ff
    )

    embed_image.set_author(
        name=inicialConfig.bot.user.name,
        icon_url=inicialConfig.bot.user.avatar
    )

    embed_image.set_footer(
        text="Feito por " + inicialConfig.bot.user.name,
        icon_url=inicialConfig.bot.user.avatar
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

    await ctx.send(embed=embed_image)


# o método run usara o token do bot como parâmetro
inicialConfig.bot.run(inicialConfig.TOKEN_DISCORD_BOT)
