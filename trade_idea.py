import guishark_msg
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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
renko_wdo = 7
renko_win = 17
renko_acoes = 100

tick_wdo = 0.5
tick_win = 5
tick_acoes = 0.01

stop_padrao_wdo = tick_wdo * (3 * renko_wdo - 1)
stop_padrao_win = tick_win * (3 * renko_win - 1)

# ENTRADA DE DADOS
###############################################################################
ativo = 'WIN'
tipo_short = 'V'
entrada = 117435

# ENTRADA DE DADOS PADRÃO
###############################################################################
if tipo_short == 'C':
    tipo = 'Compra'
elif tipo_short == 'V':
    tipo = 'Venda'
setup_op = 'Normal'
stop_tipo = 'preço'

# CONFIGURAÇÃO DE STOP PADRÃO
###############################################################################
# Stop baseado em preço
if stop_tipo == 'preço':    
    if ativo == 'WDO' and tipo == 'Compra':
        stop = entrada - stop_padrao_wdo
    elif ativo == 'WDO' and tipo == 'Venda':
        stop = entrada + stop_padrao_wdo
    elif ativo == 'WIN' and tipo == 'Compra':
        stop = entrada - stop_padrao_win
    elif ativo == 'WIN' and tipo == 'Venda':
        stop = entrada + stop_padrao_win

# Stop em pontos
if stop_tipo == 'pontos':
    if ativo == 'WDO':
        stop = stop_padrao_wdo
    elif ativo == 'WIN':
        stop = stop_padrao_win

# ENVIO DE MENSAGENS E ATUALIZAÇÃO DE DADOS    
###############################################################################
with open('trade_id.txt') as f:
    last_trade_id = f.read()

if tipo == 'Compra':
    confirmacao = confirmacao_padrao_compra
elif tipo == 'Venda':
    confirmacao = confirmacao_padrao_venda

if setup_op == 'TF':
    setup_op = 'Tendência Insider'
    
    if ativo == 'WDO':
        tick = tick_wdo
        base = renko_wdo * tick_wdo - tick_wdo
        virada = base*3 + tick
    elif ativo == 'WIN':
        tick = tick_win
        base = renko_win * tick_win - tick_win
        virada = base*3 + tick
    else:
        tick = 0.01
        
    if tipo == 'Venda':
        confirmacao = confirmacao_padrao_venda
        entrada = entrada - base - tick
        stop = entrada + virada
        alvo_1 = entrada - virada
        alvo_2 = entrada - virada*2
        alvo_3 = entrada - virada*3
    elif tipo == 'Compra':
        confirmacao = confirmacao_padrao_compra
        entrada = entrada + base + tick
        stop = entrada - virada
        alvo_1 = entrada + virada
        alvo_2 = entrada + virada*2
        alvo_3 = entrada + virada*3
    else:
        print('Erro: tipo de operação não definido')
        
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

else:
    
    if stop_tipo == 'preço':
        
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
    
    elif stop_tipo == 'pontos':
        
        
        if ativo == 'WDO':
            renko = renko_wdo * tick_wdo - tick_wdo
        elif ativo == 'WIN':
            renko = renko_win * tick_win - tick_win
            
        alvo_1 = stop
        alvo_2 = stop*2
        alvo_3 = stop*3
        entrada_1 = entrada - renko
        entrada_2 = entrada + renko
        
        tipo_op = f'💰 {tipo}: Intervalo - '\
            f'{locale.format_string("%.2f", entrada_1, grouping=True, monetary=True)} a '\
            f'{locale.format_string("%.2f", entrada_2, grouping=True, monetary=True)}\n\n'
        stop_txt = '🛑 Stop: '\
                f'{locale.format_string("%.2f", stop, grouping=True, monetary=True)} pontos\n\n'
        alvo_1_txt = '🎯 Alvo 1: '\
                f'{locale.format_string("%.2f", alvo_1, grouping=True, monetary=True)} pontos\n\n'
        alvo_2_txt = '🎯 Alvo 2: '\
                f'{locale.format_string("%.2f", alvo_2, grouping=True, monetary=True)} pontos\n\n'
        alvo_3_txt = '🎯 Alvo 3: '\
                f'{locale.format_string("%.2f", alvo_3, grouping=True, monetary=True)} pontos\n\n'

# msg = f'🚨 Ideia de Trade #{last_trade_id} - {ativo}\n\n'\
#     f'{tipo_op}'\
#     f'💻 Setup: {setup_op}\n\n'\
#     f'🤑 Confirmação: {confirmacao}\n\n'\
#     f'{stop_txt}'\
#     f'{alvo_1_txt}'\
#     f'{alvo_2_txt}'\
#     f'{alvo_3_txt}'\
#     f'{aviso_1}\n\n'\
#     f'{aviso_2}\n\n'

msg = f'🚨 Ideia de Trade #{last_trade_id} - {ativo}\n\n'\
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

last_trade_id = int(last_trade_id) + 1
with open('trade_id.txt', 'w') as f:
    f.write(str(last_trade_id))