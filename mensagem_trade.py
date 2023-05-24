import guishark_msg

def send_trade_idea_messages(mensagem, id_trade, ativo):
    
    if ativo == 'WDO':
        ativo_msg = '🇺🇸 WDO'
    elif ativo == 'WIN':
        ativo_msg = '🇧🇷 WIN'
    
    if mensagem == "Acionada":
        msg = f'Ideia de Trade #{id_trade} - {ativo_msg} - Acionada'
    elif mensagem == "Descartada":
        msg = f'Ideia de Trade #{id_trade} - {ativo_msg} - Descartada'
    elif mensagem == "Breakeven":
        msg = f'Ideia de Trade #{id_trade} - {ativo_msg} - 0 a 0 - Encerrada'
    elif mensagem == "Stop":
        msg = f'Ideia de Trade #{id_trade} - {ativo_msg} - Stop - Encerrada'
    elif mensagem == "Alvo 1":
        msg = f'Ideia de Trade #{id_trade} - {ativo_msg} - Alvo 1 - Atingido'
    elif mensagem == "Alvo 2":
        msg = f'Ideia de Trade #{id_trade} - {ativo_msg} - Alvo 2 - Atingido'
    elif mensagem == "Alvo 3":
        msg = f'Ideia de Trade #{id_trade} - {ativo_msg} - Alvo 3 - Atingido'
    elif mensagem == "Ideia Encerrada":
        msg = f'Ideia de Trade #{id_trade} - {ativo_msg} - Encerrada'

    with open('bot_token.txt') as f:
        token = f.read()
    with open('chat_id.txt') as f:
        chat_id = f.read()

    guishark_msg.send_message(token, chat_id, msg)