import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import getDados 

name = None


def input_name():
    largura_janela = 300
    altura_janela = 50
    
    def get_name():
        global name
        name = entry_nome.get() 
        if not name:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    
    largura_window = root.winfo_screenwidth()
    altura_window = root.winfo_screenheight()
    pos_x = (largura_window - largura_janela) // 2
    pos_y = (altura_window - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", get_name)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    root.protocol("WM_DELETE_WINDOW", get_name)
    botao = tk.Button(root, text="Enviar", command=get_name)
    botao.pack()

    root.mainloop()
    
    
def dead_window():
    root = tk.Tk()
    root.title("Log das Partidas")

    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    log_partidas = getDados()
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()