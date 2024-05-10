# -*- coding: utf-8 -*-
import initialSettings




states_BTC_price = list()
pilha = list()


class Rodada:
    """Essa classe vai controlar o número de vezes que espera a entrada do usuário"""
    def __init__(self) -> None:
        self.vezes = 1



class BotState:
    """Essa classe vai servir como um classe de status para o bot"""
    def __init__(self) -> None:
        self.rodada = Rodada()
        self.parar = False



class RodadaManager:
    """A classe RodadaManager vai servir para gerenciar os loop da entrada do usuário do comando !/code"""
    def __init__(self, bot_state: BotState) -> None:
        self.bot_state = bot_state

    async def process_message(self, message):
        # Se o numero de vezes que o bot ler essas mensagens for iqual a 2
        # esse bot so retorna um vazio
        if self.bot_state.rodada.vezes == 2:
            return

        if message.author == initialSettings.bot.user:
        # Vai verificar para para ver se o bot não mandou sua propria mensagem 
            return

        await message.channel.send(
            f'```{message.content}```'
            # Ele vai formatar 
        )
        await message.delete()
            # Apagar a mensagem anterior
        self.bot_state.rodada.vezes += 1
            # E vai incrementar 1 nao estado do bot


class BotContext:
    """Essa classe vai servir para gerenciar o contexto do bot"""
    def __init__(self) -> None:
        self.bot_state = BotState()


    async def process_message(self, message):
    #  ele vai mandar o contexto e mandar para o processo RodadaManager para formatar 
        rodada_manager = RodadaManager(self.bot_state)
        await rodada_manager.process_message(message)


def formatação(preço):
    # Essa função vai usar o replace para formatar 
    # o float para o tipo de moeda BRL
    valor_formatação_padrao = f'{preço:,.2f}'
    valor = valor_formatação_padrao.replace('.', ',',1)
    # vai somente uma vez substituir pontos por virgulas
    return valor.replace(',', '.',valor_formatação_padrao.count(','))
    # o "count" para contar o número de partes inteiras para trocar por pontos  
