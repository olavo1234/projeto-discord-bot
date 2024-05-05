import inicialConfig


states_BTC_price = list()
pilha = list()


ID_USER = 953750556625739826

server_channel_mapping = {
    'ozu': 964952312307142749,
}


palavrões = ['caralho', 'porra',
            'puta que pariu', 'merda',
            'puta merda', 'cacete', 'foder',
            'fudeu', 'filho da puta', 'filha da puta',
            'puta'
        ]


class Rodada:
    # essa classe vai controlar o numero de vezes
    # que espera a entrada do usuario
    def __init__(self) -> None:
        self.vezes = 1



class BotState:
    def __init__(self) -> None:
        self.rodada = Rodada()
        self.parar = False



class RodadaManager:
    def __init__(self, bot_state: BotState) -> None:
        self.bot_state = bot_state

    async def process_message(self, message):
        if self.bot_state.rodada.vezes == 2:
            return

        if message.author == inicialConfig.bot.user:
            return

        await message.channel.send(
            f'```{message.content}```'
        )
        await message.delete()
        self.bot_state.rodada.vezes += 1


class BotContext:
    def __init__(self) -> None:
        self.bot_state = BotState()


    async def process_message(self, message):
        rodada_manager = RodadaManager(self.bot_state)
        await rodada_manager.process_message(message)


def formatação(preço):
    valor_formatação_padrao = f'{preço:,.2f}'
    valor = valor_formatação_padrao.replace('.', ',',1)
    return valor.replace(',', '.',valor_formatação_padrao.count(','))
