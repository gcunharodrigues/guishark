import guishark_msg
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def send_trade_idea(renko_wdo, renko_win, ativo, tipo, entrada, last_trade_id):
    # AVISOS
    ###############################################################################
    aviso_1 = 'Abra a sua conta no BTG: http://www.uriel.pro/btg'
    aviso_2 = 'Disclaimer : As ideias de trade tem o objetivo educacional '\
    'para suscitar o exercício do trader a tomar a sua própria decisão de '\
    'operação, não constituindo qualquer tipo de oferta ou solicitação de '\
    'compra e/ou venda de qualquer produto.'

    # MENSAGENS PADRÃO
    ###############################################################################
    confirmacao_padrao_compra = 'Vendedores tentarem consumir a liquidez e '\
    'Compradores continuar fornecendo (Renovação, absorção, agressão e/ou piora de '\
    'lote por parte dos Compradores).'
    confirmacao_padrao_venda = 'Compradores tentarem consumir a liquidez e '\
    'Vendedores continuar fornecendo (Renovação, absorção, agressão e/ou piora de '\
    'lote por parte dos Vendedores).'

    # PADRÕES ATIVOS
    ###############################################################################
    tick_wdo = 0.5
    tick_win = 5
    tick_acoes = 0.01

    stop_padrao_wdo = tick_wdo * (3 * renko_wdo - 2) + tick_wdo
    stop_padrao_win = tick_win * (3 * renko_win - 2) + tick_win

    # CONFIGURAÇÃO DE STOP PADRÃO
    ###############################################################################
    if ativo == 'WDO' and tipo == 'Compra':
        stop = entrada - stop_padrao_wdo
    elif ativo == 'WDO' and tipo == 'Venda':
        stop = entrada + stop_padrao_wdo
    elif ativo == 'WIN' and tipo == 'Compra':
        stop = entrada - stop_padrao_win
    elif ativo == 'WIN' and tipo == 'Venda':
        stop = entrada + stop_padrao_win

    # ENVIO DE MENSAGENS E ATUALIZAÇÃO DE DADOS    
    ###############################################################################
    if tipo == 'Compra':
        confirmacao = confirmacao_padrao_compra
    elif tipo == 'Venda':
        confirmacao = confirmacao_padrao_venda
            
    if tipo == 'Venda':
        virada = stop - entrada
        alvo_1 = entrada - virada
        alvo_2 = entrada - virada*2
        alvo_3 = entrada - virada*3
    elif tipo == 'Compra':
        virada = entrada - stop
        alvo_1 = entrada + virada
        alvo_2 = entrada + virada*2
        alvo_3 = entrada + virada*3
            
    tipo_op = f'💰 {tipo}: '\
            f'{locale.format_string("%.2f", entrada, grouping=True, monetary=True)}\n\n'
    stop_txt = '🛑 Stop: '\
            f'{locale.format_string("%.2f", stop, grouping=True, monetary=True)}\n\n'
    alvo_1_txt = '🎯 Alvo 1: '\
            f'{locale.format_string("%.2f", alvo_1, grouping=True, monetary=True)}\n\n'
    alvo_2_txt = '🎯 Alvo 2: '\
            f'{locale.format_string("%.2f", alvo_2, grouping=True, monetary=True)}\n\n'
    alvo_3_txt = '🎯 Alvo 3: '\
            f'{locale.format_string("%.2f", alvo_3, grouping=True, monetary=True)}\n\n'
    
    if ativo == 'WDO':
        ativo_msg = '🇺🇸 WDO'
    elif ativo == 'WIN':
        ativo_msg = '🇧🇷 WIN'
        
    msg = f'🚨 Ideia de Trade #{last_trade_id} - {ativo_msg}\n\n'\
        f'{tipo_op}'\
        f'🤑 Confirmação: {confirmacao}\n\n'\
        f'{stop_txt}'\
        f'{alvo_1_txt}'\
        f'{alvo_2_txt}'\
        f'{alvo_3_txt}'\
        f'{aviso_1}\n\n'\
        f'{aviso_2}\n\n'

    with open('bot_token.txt') as f:
        token = f.read()
    with open('chat_id.txt') as f:
        chat_id = f.read()

    guishark_msg.send_message(token, chat_id, msg)
    
    return stop, alvo_1, alvo_2, alvo_3