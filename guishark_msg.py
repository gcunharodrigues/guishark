# importar biblioteca para requisições http
import requests

# mostra o id do último grupo adicionado
def last_chat_id(token):
    try:
        url = "https://api.telegram.org/bot{}/getUpdates".format(token)
        response = requests.get(url)
        if response.status_code == 200:
            json_msg = response.json()
            print(json_msg)
            for json_result in reversed(json_msg['result']):
                message_keys = json_result['message'].keys()
                if ('new_chat_member' in message_keys) or ('group_chat_created' in message_keys):
                    return json_result['message']['chat']['id']
            print('Nenhum grupo encontrado')
        else:
            print('A resposta falhou, código de status: {}'.format(response.status_code))
    except Exception as e:
        print("Erro no getUpdates:", e)

# enviar mensagens utilizando o bot para um chat específico
def send_message(token, chat_id, message):
    try:
        data = {"chat_id": chat_id, "text": message, 
                "disable_web_page_preview": 1,} #, "parse_mode": 'markdown'}
        url = "https://api.telegram.org/bot{}/sendMessage".format(token)
        requests.post(url, data)
        print("Mensagem Enviada")
    except Exception as e:
        print("Erro no sendMessage:", e)

# escrever em arquivo o chat_id do último grupo adicionado
def write_chat_id(token):
    # id do chat que será enviado as mensagens
    chat_id = last_chat_id(token)
    with open('chat_id.txt', 'w') as f:
        f.write(str(chat_id))
        print("Id do chat:", chat_id)

# token único utilizado para manipular o bot (não deve ser compartilhado)
# exemplo: '1413778757:AAFxmr611LssAHbZn1uqV_NKFsbwK3TT-'
# token = ''
# chat_id = ''

# exemplo de mensagem
# msg = "Teste"

# enviar a mensagem
# send_message(token, chat_id, msg)
# last_chat_id(token)
