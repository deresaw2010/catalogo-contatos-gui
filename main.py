# main.py

import tkinter as tk
from tkinter import messagebox
import contatos

class ContatoForm(tk.Toplevel):
    def __init__(self, master, titulo, contato=None, on_submit=None):
        super().__init__(master)
        self.title(titulo)
        self.on_submit = on_submit
        self.resizable(False, False)

        # Campos
        self.vars = {
            "nome": tk.StringVar(value=contato['nome'] if contato else ""),
            "endereco": tk.StringVar(value=contato['endereco'] if contato else ""),
            "telefone": tk.StringVar(value=contato['telefone'] if contato else ""),
            "email": tk.StringVar(value=contato['email'] if contato else "")
        }

        for i, campo in enumerate(self.vars):
            tk.Label(self, text=campo.capitalize()).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Entry(self, textvariable=self.vars[campo], width=40).grid(row=i, column=1, padx=10)

        tk.Button(self, text="Salvar", command=self.submit).grid(row=4, column=0, columnspan=2, pady=10)

    def submit(self):
        dados = {k: v.get().strip() for k, v in self.vars.items()}
        if not dados["nome"]:
            messagebox.showwarning("Erro", "O nome é obrigatório.")
            return
        if self.on_submit:
            self.on_submit(dados)
        self.destroy()

class AgendaApp:
    def __init__(self, master):
        self.master = master
        master.title("Agenda de Contatos")

        # Botões
        tk.Button(master, text="Adicionar Contato", command=self.adicionar_contato).pack(fill=tk.X)
        tk.Button(master, text="Listar Contatos", command=self.listar_contatos).pack(fill=tk.X)
        tk.Button(master, text="Buscar Contato", command=self.buscar_contato).pack(fill=tk.X)
        tk.Button(master, text="Editar Contato", command=self.editar_contato).pack(fill=tk.X)
        tk.Button(master, text="Excluir Contato", command=self.excluir_contato).pack(fill=tk.X)
        tk.Button(master, text="Sair", command=master.quit).pack(fill=tk.X)

        # Área de exibição
        self.texto = tk.Text(master, height=20, width=80)
        self.texto.pack(pady=10)

    def limpar_texto(self):
        self.texto.delete('1.0', tk.END)

    def exibir_contatos(self, lista):
        self.limpar_texto()
        if not lista:
            self.texto.insert(tk.END, "Agenda vazia.\n")
        else:
            for i, c in enumerate(lista):
                self.texto.insert(tk.END, f"{i + 1}. {c['nome']} - {c['telefone']} - {c['email']}\n")

    def adicionar_contato(self):
        def salvar(dados):
            contatos.adicionar_contato(**dados)
            messagebox.showinfo("Sucesso", "Contato adicionado com sucesso!")

        ContatoForm(self.master, "Adicionar Contato", on_submit=salvar)

    def listar_contatos(self):
        lista = contatos.listar_contatos()
        self.exibir_contatos(lista)

    def buscar_contato(self):
        nome = tk.simpledialog.askstring("Buscar", "Digite o nome do contato:")
        if not nome:
            return
        encontrados = contatos.buscar_contato_por_nome(nome)
        self.limpar_texto()
        if encontrados:
            for c in encontrados:
                self.texto.insert(tk.END,
                    f"Nome: {c['nome']}\nEndereço: {c['endereco']}\nTelefone: {c['telefone']}\nEmail: {c['email']}\n---\n")
        else:
            self.texto.insert(tk.END, "Contato não encontrado.\n")

    def editar_contato(self):
        nome = tk.simpledialog.askstring("Editar", "Digite o nome do contato a editar:")
        if not nome:
            return
        resultado = contatos.buscar_contato_por_nome(nome)
        if not resultado:
            messagebox.showwarning("Erro", "Contato não encontrado.")
            return

        def salvar(dados):
            contatos.editar_contato(nome, dados['endereco'], dados['telefone'], dados['email'])
            messagebox.showinfo("Sucesso", "Contato editado com sucesso!")

        ContatoForm(self.master, "Editar Contato", contato=resultado[0], on_submit=salvar)

    def excluir_contato(self):
        nome = tk.simpledialog.askstring("Excluir", "Digite o nome do contato a excluir:")
        if not nome:
            return
        confirmado = messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir '{nome}'?")
        if confirmado:
            if contatos.excluir_contato(nome):
                messagebox.showinfo("Sucesso", "Contato excluído com sucesso!")
            else:
                messagebox.showwarning("Erro", "Contato não encontrado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    root.mainloop()
