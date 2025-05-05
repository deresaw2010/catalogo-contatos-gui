import tkinter as tk
from tkinter import messagebox
import contatos

# Atualiza a lista visível
def atualizar_lista():
    lista_contatos.delete(0, tk.END)
    for contato in contatos.listar_contatos():
        lista_contatos.insert(tk.END, contato["nome"])

# Formulário unificado para adicionar ou editar
def abrir_formulario_contato(titulo, contato_existente=None, callback=None):
    def salvar():
        nome = entry_nome.get().strip()
        endereco = entry_endereco.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()

        if not nome:
            messagebox.showerror("Erro", "O campo 'nome' é obrigatório.")
            return

        if callback:
            callback(nome, endereco, telefone, email)
        janela_form.destroy()

    janela_form = tk.Toplevel(janela)
    janela_form.title(titulo)
    janela_form.grab_set()

    tk.Label(janela_form, text="Nome:").grid(row=0, column=0, sticky="e")
    entry_nome = tk.Entry(janela_form, width=40)
    entry_nome.grid(row=0, column=1)

    tk.Label(janela_form, text="Endereço:").grid(row=1, column=0, sticky="e")
    entry_endereco = tk.Entry(janela_form, width=40)
    entry_endereco.grid(row=1, column=1)

    tk.Label(janela_form, text="Telefone:").grid(row=2, column=0, sticky="e")
    entry_telefone = tk.Entry(janela_form, width=40)
    entry_telefone.grid(row=2, column=1)

    tk.Label(janela_form, text="Email:").grid(row=3, column=0, sticky="e")
    entry_email = tk.Entry(janela_form, width=40)
    entry_email.grid(row=3, column=1)

    if contato_existente:
        entry_nome.insert(0, contato_existente["nome"])
        entry_endereco.insert(0, contato_existente["endereco"])
        entry_telefone.insert(0, contato_existente["telefone"])
        entry_email.insert(0, contato_existente["email"])

    btn_salvar = tk.Button(janela_form, text="Salvar", command=salvar)
    btn_salvar.grid(row=4, column=0, columnspan=2, pady=10)

# Adicionar contato
def adicionar_contato():
    def adicionar_callback(nome, endereco, telefone, email):
        contatos.adicionar_contato(nome, endereco, telefone, email)
        atualizar_lista()
    abrir_formulario_contato("Adicionar Contato", callback=adicionar_callback)

# Editar contato
def editar_contato():
    selecionado = lista_contatos.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um contato para editar.")
        return
    i = selecionado[0]
    contato_atual = contatos.listar_contatos()[i]

    def editar_callback(nome, endereco, telefone, email):
        contatos.editar_contato(nome, endereco, telefone, email)
        atualizar_lista()
    abrir_formulario_contato("Editar Contato", contato_atual, callback=editar_callback)

# Excluir contato
def excluir_contato():
    selecionado = lista_contatos.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um contato para excluir.")
        return
    i = selecionado[0]
    contato = contatos.listar_contatos()[i]
    confirm = messagebox.askyesno("Confirmação", f"Excluir o contato '{contato['nome']}'?")
    if confirm:
        contatos.excluir_contato(contato["nome"])
        atualizar_lista()

# Ver detalhes
def mostrar_detalhes(event=None):
    selecionado = lista_contatos.curselection()
    if not selecionado:
        return
    i = selecionado[0]
    contato = contatos.listar_contatos()[i]
    detalhes = (
        f"Nome: {contato['nome']}\n"
        f"Endereço: {contato['endereco']}\n"
        f"Telefone: {contato['telefone']}\n"
        f"Email: {contato['email']}"
    )
    messagebox.showinfo("Detalhes do Contato", detalhes)

# Janela principal
janela = tk.Tk()
janela.title("Agenda de Contatos")

lista_contatos = tk.Listbox(janela, width=40, height=10)
lista_contatos.pack(pady=10)
lista_contatos.bind("<Double-Button-1>", mostrar_detalhes)

frame_botoes = tk.Frame(janela)
frame_botoes.pack()

tk.Button(frame_botoes, text="Adicionar", command=adicionar_contato).grid(row=0, column=0, padx=5)
tk.Button(frame_botoes, text="Editar", command=editar_contato).grid(row=0, column=1, padx=5)
tk.Button(frame_botoes, text="Excluir", command=excluir_contato).grid(row=0, column=2, padx=5)
tk.Button(frame_botoes, text="Ver Detalhes", command=mostrar_detalhes).grid(row=0, column=3, padx=5)

atualizar_lista()
janela.mainloop()
