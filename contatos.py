# contatos.py

agenda = []

def adicionar_contato(nome, endereco, telefone, email):
    contato = {
        "nome": nome,
        "endereco": endereco,
        "telefone": telefone,
        "email": email
    }
    agenda.append(contato)

def listar_contatos():
    return agenda.copy()

def buscar_contato_por_nome(nome):
    return [c for c in agenda if c['nome'].lower() == nome.lower()]

def editar_contato(nome, novo_endereco=None, novo_telefone=None, novo_email=None):
    for contato in agenda:
        if contato['nome'].lower() == nome.lower():
            if novo_endereco:
                contato['endereco'] = novo_endereco
            if novo_telefone:
                contato['telefone'] = novo_telefone
            if novo_email:
                contato['email'] = novo_email
            return True
    return False

def excluir_contato(nome):
    for i, contato in enumerate(agenda):
        if contato['nome'].lower() == nome.lower():
            del agenda[i]
            return True
    return False
