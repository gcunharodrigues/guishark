from tkinter import *
from PIL import Image, ImageTk
import subprocess
import os
#import trade_idea_v1
import trade_idea_v2
import mensagem_trade

root = Tk()
root.title('WDO - Shark AlgoBot')

#global wdo_renko, win_renko, id_trade, ativo_trade, tipo_trade
global wdo_stop, win_stop, id_trade, ativo_trade, tipo_trade
global entrada_trade, stop, alvo_1, alvo_2, alvo_3

wdo_stop = None
win_stop = 0
id_trade = None
ativo_trade = None
tipo_trade = None
entrada_trade = None
stop = None
alvo_1 = None
alvo_2 = None   
alvo_3 = None

def open_profitchart():
    subprocess.Popen(["C:/Users/guicr/AppData/Roaming/Nelogica/Profit/profitchart.exe"])
        
def open_planilha():
    os.system('start excel.exe "C:/Users/guicr/OneDrive/Work/UrielShark/db_trades.xlsx"')
    
def open_textos():
    subprocess.Popen([r"C:/Program Files/Notepad++/notepad++.exe",r"C:/Users/guicr/OneDrive/Work/UrielShark/textos_padrao.txt"])
    
frame1_label = Label(root, text="Início", font=("Arial", 15)).grid(row=0, column=0,
                                                   columnspan=4)
    
open_profitchart = Button(root, text="Abrir Profitchart", command=open_profitchart)
open_profitchart.grid(row=1, column=0)

wdo_label = Label(root, text="WDO").grid(row=3, column=1)
ativo_label = Label(root, text="Ativo:").grid(row=3, column=0)
    
open_planilha = Button(root, text="Abrir Planilha", command=open_planilha)
open_planilha.grid(row=1, column=1)

open_textos = Button(root, text="Abrir Textos", command=open_textos)
open_textos.grid(row=1, column=2)

def get_ideia_data():
    global id_dado_label, ativo_dado_label, tipo_dado_label, entrada_dado_label
    global stop_dado_label, alvo1_dado_label, alvo2_dado_label, alvo3_dado_label
    
    wdo_stop = wdo_entry_data.get()
    id_trade = id_entry_data.get()
    ativo_trade = ativo2_menu.get()
    tipo_trade = tipo_menu.get()
    entrada_trade = entrada_entry_data.get()
    
    id_trade = 'WDO_' + id_trade
    
    stop, alvo_1, alvo_2, alvo_3 = trade_idea_v2.send_trade_idea(float(wdo_stop), 
                                  int(win_stop), 
                                  ativo_trade, 
                                  tipo_trade, 
                                  float(entrada_trade),
                                  id_trade)
    
    with open('trade_info_wdo.txt', 'w') as f:
        f.write(f'{id_trade}\n')
        f.write(f'{ativo_trade}')
    
    id_dado_label.destroy()
    ativo_dado_label.destroy()
    tipo_dado_label.destroy()
    entrada_dado_label.destroy()
    
    id_dado_label = Label(root, text=id_trade)
    id_dado_label.grid(row=11, column=1)
    ativo_dado_label = Label(root, text=ativo_trade)
    ativo_dado_label.grid(row=12, column=1)
    tipo_dado_label = Label(root, text=tipo_trade)
    tipo_dado_label.grid(row=13, column=1)
    entrada_dado_label = Label(root, text=entrada_trade)
    entrada_dado_label.grid(row=14, column=1)

    stop_dado_label.destroy()
    alvo1_dado_label.destroy()
    alvo2_dado_label.destroy()
    alvo3_dado_label.destroy()
    
    stop_dado_label = Label(root, text=stop)
    stop_dado_label.grid(row=11, column=4)
    alvo1_dado_label = Label(root, text=alvo_1)
    alvo1_dado_label.grid(row=12, column=4)
    alvo2_dado_label = Label(root, text=alvo_2)
    alvo2_dado_label.grid(row=13, column=4)
    alvo3_dado_label = Label(root, text=alvo_3)
    alvo3_dado_label.grid(row=14, column=4)
    
    id_entry.delete(0, END)
    ativo2_menu.set("WDO")
    tipo_menu.set("Nenhum")
    entrada_entry.delete(0, END)

      
frame2_label = Label(root, text="Ideia de Trade", font=("Arial", 15)).grid(row=5, column=0,
                                                        columnspan=4)
     
id_label = Label(root, text="ID:")
id_label.grid(row=6, column=0)
ativo2_label = Label(root, text="Ativo:")
ativo2_label.grid(row=7, column=0)
tipo_label = Label(root, text="Tipo:")
tipo_label.grid(row=8, column=0)
entrada_label = Label(root, text="Entrada:")
entrada_label.grid(row=9, column=0)

stop_label = Label(root, text="Stop:").grid(row=4, column=0)
wdo_entry_data = StringVar()
wdo_entry = Entry(root, textvariable=wdo_entry_data ,width=5)
wdo_entry.grid(row=4, column=1)

id_entry_data = StringVar()    
id_entry = Entry(root, textvariable=id_entry_data,width=5)
id_entry.grid(row=6, column=1)
    
ativo2_menu = StringVar()
ativos2 = ["WDO"]
# ativos2 = ["Nenhum", "WDO", "WIN"]
ativo2_menu.set("WDO")
ativo2_entry = OptionMenu(root, ativo2_menu, *ativos2).grid(row=7, column=1)
    
tipo_menu = StringVar()
tipos = ["Nenhum", "Compra", "Venda"]
tipo_menu.set("Nenhum")
tipo_entry = OptionMenu(root, tipo_menu, *tipos).grid(row=8, column=1)

entrada_entry_data = StringVar()    
entrada_entry = Entry(root, textvariable=entrada_entry_data,width=10)
entrada_entry.grid(row=9, column=1)
    
send_button = Button(root, text="Enviar", pady=50, 
                         command=get_ideia_data).grid(row=6, column=2, 
                                                            rowspan=4)

frame2_label = Label(root, text="Ideia Atual", 
                    font=("Arial", 15))
frame2_label.grid(row=10, column=0,
                                                    columnspan=4)
    
id_atual_label = Label(root, text="ID:")
id_atual_label.grid(row=11, column=0)
ativo_atual_label = Label(root, text="Ativo:").grid(row=12, column=0)
tipo_atual_label = Label(root, text="Tipo:").grid(row=13, column=0)
entrada_atual_label = Label(root, text="Entrada:").grid(row=14, column=0)
mensagem_label = Label(root, text="Mensagem:").grid(row=15, column=0)
    
stop_label = Label(root, text="Stop:").grid(row=11, column=2)
alvo1_label = Label(root, text="Alvo 1:").grid(row=12, column=2)
alvo2_label = Label(root, text="Alvo 2:").grid(row=13, column=2)
alvo3_label = Label(root, text="Alvo 3:").grid(row=14, column=2)
    
id_dado_label = Label(root, text=id_trade)
id_dado_label.grid(row=11, column=1)
ativo_dado_label = Label(root, text=ativo_trade)
ativo_dado_label.grid(row=12, column=1)
tipo_dado_label = Label(root, text=tipo_trade)
tipo_dado_label.grid(row=13, column=1)
entrada_dado_label = Label(root, text=entrada_trade)
entrada_dado_label.grid(row=14, column=1)
    
stop_dado_label = Label(root, text=stop)
stop_dado_label.grid(row=11, column=4)
alvo1_dado_label = Label(root, text=alvo_1)
alvo1_dado_label.grid(row=12, column=4)
alvo2_dado_label = Label(root, text=alvo_2)
alvo2_dado_label.grid(row=13, column=4)
alvo3_dado_label = Label(root, text=alvo_3)
alvo3_dado_label.grid(row=14, column=4)

def send_messages_trade_idea():
    mensagem = mensagem_menu.get()
    
    with open('trade_info_wdo.txt', 'r', newline='') as f:
        lines = [line.rstrip() for line in f]
            
    id_trade = lines[0]
    ativo_trade = lines[1]
    
    mensagem_trade.send_trade_idea_messages(mensagem, id_trade, ativo_trade)
    mensagem_menu.set("Nenhuma")
    
mensagens = [
    "Nenhuma",
    "Acionada",
    "Descartada",
    "Stop",
    "Breakeven",
    "Alvo 1",
    "Alvo 2",
    "Alvo 3",
    "Ideia Encerrada"
    ]
mensagem_menu = StringVar()
mensagem_menu.set("Nenhuma")
mensagem_entry = OptionMenu(root, mensagem_menu, *mensagens).grid(row=15, 
                                                                    column=1)
    
send_message_button = Button(root, text="Enviar mensagem", 
                             command=send_messages_trade_idea).grid(row=15,
                                                                column=2)
           

root.mainloop()