#Conexão com o banco e criação das tabelas
import  sqlite3

conn = sqlite3.connect('database/tm.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id integer primary key, nome varchar(50), email varchar(50))")
cursor.execute("CREATE TABLE IF NOT EXISTS tarefas (id integer primary key, titulo varchar(70), status varchar(10), usuario_id integer, foreign key(usuario_id) references usuarios(id))")
conn.commit()

#Funções utilizadas (CRUD)
def cadastro():
    nome = input("Nome do usuario: ")
    email = input("Email do usuario: ")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    print("Usuário cadastrado com sucesso!")

def listar_usuarios():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    lista = cursor.fetchall()
    if lista != []:
        for usuario in lista:
            print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}")
    else:
        print("Nenhum usuário cadastrado.")

def buscar_usuario():
    id_usuario = int(input("ID do usuario: "))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
    lista = cursor.fetchone()
    if lista != None:
        print(f"ID: {lista[0]}, Nome: {lista[1]}, Email: {lista[2]}")
    else:
        print("Usuário não encontrado.")

def cadastrar_tarefa():
    titulo = input("Digite o titulo da tarefa: ")
    if titulo != "":
        cursor = conn.cursor()
    else:
        print("Título inválido! Retornando ao menu...")
        return False
    id_responsavel = int(input("Digite a id do usuário responsável pela tarefa: "))
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_responsavel,))
    usuario = cursor.fetchone()
    if usuario != None:
        nome = usuario[1]
        print(f"Deseja cadastrar uma tarefa para o usuário: {nome}?\n[S] Sim\n[N] Não\n")
        resposta = input()
        resposta = resposta.upper()
        if resposta == "S":
            status = "Pendente"
            cursor.execute("INSERT INTO tarefas (titulo, usuario_id, status) VALUES (?, ?, ?)", (titulo, id_responsavel, status,))
            print("Tarefa cadastrada com sucesso!")
            conn.commit()
        elif resposta == "N":
            print("Operação cancelada. Retornando ao menu...")
        else:
            print("Opção inválida! Retornando ao menu...")
    else:
        print("Usuário não encontrado. Retornando ao menu...")

def listar_tarefas():
    cursor = conn.cursor()
    cursor.execute("SELECT tarefas.id, tarefas.titulo, tarefas.status, usuarios.nome   "
                   "FROM tarefas   "
                   "INNER JOIN usuarios   "
                   "ON tarefas.usuario_id = usuarios.id; ")
    lista = cursor.fetchall()
    if lista != []:
        for tarefa in lista:
            print(f"ID: {tarefa[0]}, Título: {tarefa[1]}, Status: {tarefa[2]}, Usuário: {tarefa[3]}")
    else:
        print("Nenhuma tarefa cadastrada.")

def atualizar_tarefa():
    cursor = conn.cursor()
    id_tarefa = int(input("Digite o id da tarefa: "))
    cursor.execute("SELECT tarefas.id, tarefas.titulo, usuarios.nome   "
                   "FROM tarefas   "
                   "INNER JOIN usuarios   "
                   "ON tarefas.usuario_id = usuarios.id   "
                   "WHERE tarefas.id = ?;", (id_tarefa,))
    tarefa = cursor.fetchone()
    if tarefa != None:
        print(f"Deseja marcar a tarefa {tarefa[1]} do usuário {tarefa[2]} como concluída?\n[S] Sim\n[N] Não\n")
        escolha = input()
        escolha = escolha.upper()
        if escolha == "S":
            cursor.execute("UPDATE tarefas   "
                           "SET status = 'Concluída'   "
                           "WHERE id = ?;   ", (id_tarefa,))
            conn.commit()
        elif escolha == "N":
            print("Retornando ao menu...")
        else:
            print("Opção inválida. Retornando ao menu...")
    else:
        print("Nenhuma tarefa encontrada. Retornando ao menu...")

def excluir_tarefa():
    cursor = conn.cursor()
    id_tarefa = int(input("Digite o id da tarefa: "))
    cursor.execute("SELECT tarefas.id, tarefas.titulo, usuarios.nome   "
                   "FROM tarefas   "
                   "INNER JOIN usuarios   "
                   "ON tarefas.usuario_id = usuarios.id   "
                   "WHERE tarefas.id = ?;", (id_tarefa,))
    tarefa = cursor.fetchone()
    if tarefa != None:
        print(f"Deseja excluir a tarefa {tarefa[1]}?\n[S] Sim\n[N] Não\n")
        escolha = input()
        escolha = escolha.upper()
        if escolha == "S":
            cursor.execute("DELETE FROM tarefas WHERE id = ?; ", (id_tarefa,))
            conn.commit()
        elif escolha == "N":
            print("Retornando ao menu...")
        else:
            print("Opção inválida. Retornando ao menu...")
    else:
        print("Tarefa não encontrada. Retornando ao menu...")

#Menu principal
op = 0

def menu():
    print("="*20)
    print("1. Cadastrar")
    print("2. Listar usuarios")
    print("3. Buscar usuario")
    print("4. Cadastrar tarefa")
    print("5. Listar tarefas")
    print("6. Atualizar tarefa")
    print("7. Excluir tarefa")
    print("8. Sair")
    print("=" * 20)

while op != 8:
    menu()
    op = int(input())
    if op == 1:
        cadastro()
    if op == 2:
        listar_usuarios()
    if op == 3:
        buscar_usuario()
    if op == 4:
        cadastrar_tarefa()
    if op == 5:
        listar_tarefas()
    if op == 6:
        atualizar_tarefa()
    if op == 7:
        excluir_tarefa()

if op == 8:
    print("Saindo...")
    conn.close()