import guishark_msg

with open('bot_token.txt') as f:
    token = f.read()
    
guishark_msg.write_chat_id(token)