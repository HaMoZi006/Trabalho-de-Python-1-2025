import sqlite3       #para conserguimos criar um banco de dados pelo proprio python
from datetime import datetime

def  conectar():
    return sqlite3.connect("biblioteca.db")

def criar_tabelas(): #criar as tabelas
    con = conectar()
    cur = con.cursor()
    
    #"cur" para criar todas as tebelas
    # tabelas que vamos usar: Livros, Usuario, Funcionarios e emprestimo.

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Livro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER,
        genero TEXT,
        quantidade INTEGER
    )
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE,
        endereco TEXT,
        telefone TEXT,
        email TEXT UNIQUE
    )
    ''')


    cur.execute('''
    CREATE TABLE IF NOT EXISTS Emprestimo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_livro INTEGER,
        id_funcionario INTEGER,
        data_emprestimo TEXT,
        data_prevista TEXT,
        data_devolucao TEXT,
        FOREIGN KEY (id_usuario) REFERENCES Usuario(id),
        FOREIGN KEY (id_livro) REFERENCES Livro(id),
        FOREIGN KEY (id_funcionario) REFERENCES Funcionario(id)
    )
    ''')

#------------------------------------------CRUD para LIVROS----------------------------------------------------
# (Vai servir para podermos permite criar, ler, atualizar e apagar os dados de vosso banco papai)

def adicionar_livro():
    try:
        titulo = input("Título: ")
        autor = input("Autor: ")
        ano = int(input("Ano de Publicação: "))
        genero = input("Gênero: ")
        quantidade = int(input("Quantidade disponível: "))

        con = conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO Livro (titulo, autor, ano_publicacao, genero, quantidade) VALUES (?,?,?,?,?)",
                    (titulo, autor, ano, genero, quantidade))
        con.commit()
        print("Livro adicionado com sucesso!")
    except Exception as e:
        print("Erro ao adicionar livro:", e)
    finally:
        con.close()

def listar_livros():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM Livro")
    livros = cur.fetchall()
    if livros:
        for l in livros:
            print(f"ID: {l[0]}, Título: {l[1]}, Autor: {l[2]}, Ano: {l[3]}, Gênero: {l[4]}, Quantidade: {l[5]}")
    else:
        print("Nenhum livro encontrado.")
    con.close()

def atualizar_livro():
    try:
        id_livro = int(input("ID do livro a atualizar: "))
        nova_quantidade = int(input("Nova quantidade: "))

        con = conectar()
        cur = con.cursor()
        cur.execute("UPDATE Livro SET quantidade = ? WHERE id = ?", (nova_quantidade, id_livro))
        if cur.rowcount == 0:
            print("ID não encontrado.")
        else:
            con.commit()
            print("Livro atualizado com sucesso!")
    except Exception as e:
        print("Erro ao atualizar:", e)
    finally:
        con.close()

def deletar_livro():
    try:
        id_livro = int(input("ID do livro a deletar: "))
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM Livro WHERE id = ?", (id_livro,))
        if cur.rowcount == 0:
            print("ID não encontrado.")
        else:
            con.commit()
            print("Livro deletado com sucesso!")
    except Exception as e:
        print("Erro ao deletar:", e)
    finally:
        con.close()

#-----------------------------------------CRUD para funcionarios--------------------------------------------------

def adicionar_usuario():
    try:
        nome = input("Nome: ")
        cpf = input("CPF: ")
        endereco = input("Endereço: ")
        telefone = input("Telefone: ")
        email = input("Email: ")

        con = conectar()
        cur = con.cursor()
        cur.execute('''
            INSERT INTO Usuario (nome, cpf, endereco, telefone, email)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, cpf, endereco, telefone, email))
        con.commit()
        print("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF já cadastrado.")
    except Exception as e:
        print("Erro ao adicionar usuário:", e)
    finally:
        con.close()

def listar_usuarios():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM Usuario")
    usuarios = cur.fetchall()
    if usuarios:
        for u in usuarios:
            print(f"ID: {u[0]}, Nome: {u[1]}, CPF: {u[2]}, Endereço: {u[3]}, Telefone: {u[4]}, Email: {u[5]}")
    else:
        print("Nenhum usuário encontrado.")
    con.close()

def atualizar_usuario():
    try:
        id_usuario = int(input("ID do usuário a atualizar: "))
        novo_telefone = input("Novo telefone: ")
        novo_email = input("Novo e-mail: ")

        con = conectar()
        cur = con.cursor()
        cur.execute("UPDATE Usuario SET telefone = ?, email = ? WHERE id = ?",
                    (novo_telefone, novo_email, id_usuario))
        if cur.rowcount == 0:
            print("Usuário não encontrado.")
        else:
            con.commit()
            print("Usuário atualizado com sucesso!")
    except Exception as e:
        print("Erro ao atualizar usuário:", e)
    finally:
        con.close()

def deletar_usuario():
    try:
        id_usuario = int(input("ID do usuário a deletar: "))
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM Usuario WHERE id = ?", (id_usuario,))
        if cur.rowcount == 0:
            print("Usuário não encontrado.")
        else:
            con.commit()
            print("Usuário deletado com sucesso!")
    except Exception as e:
        print("Erro ao deletar usuário:", e)
    finally:
        con.close()

#-------------------------------------------CRUD Empréstimo------------------------------------------------------

def registrar_emprestimo():
    try:
        id_usuario = int(input("ID do usuário: "))
        id_livro = int(input("ID do livro: "))
        id_funcionario = input("ID do funcionário (opcional): ")
        data_emprestimo = datetime.now().strftime("%Y-%m-%d")
        data_prevista = input("Data prevista de devolução (YYYY-MM-DD): ")

        con = conectar()
        cur = con.cursor()

        # Verificar se o livro está disponível na blibioteca
        cur.execute("SELECT quantidade FROM Livro WHERE id = ?", (id_livro,))
        resultado = cur.fetchone()
        if not resultado:
            print("Livro não encontrado.")
            return
        elif resultado[0] <= 0:
            print("Livro indisponível.")
            return

        cur.execute('''
            INSERT INTO Emprestimo (id_usuario, id_livro, id_funcionario, data_emprestimo, data_prevista, data_devolucao)
            VALUES (?, ?, ?, ?, ?, NULL)
        ''', (id_usuario, id_livro, id_funcionario or None, data_emprestimo, data_prevista))

        # Atualizar quantidade de livros disponíveis apos aluguel ou devolução 

        cur.execute("UPDATE Livro SET quantidade = quantidade - 1 WHERE id = ?", (id_livro,))
        
        con.commit()
        print("Empréstimo registrado com sucesso!")
    except Exception as e:
        print("Erro ao registrar empréstimo:", e)
    finally:
        con.close()

def listar_emprestimos():
    con = conectar()
    cur = con.cursor()
    cur.execute('''
        SELECT e.id, u.nome, l.titulo, e.data_emprestimo, e.data_prevista, e.data_devolucao
        FROM Emprestimo e
        JOIN Usuario u ON e.id_usuario = u.id
        JOIN Livro l ON e.id_livro = l.id
    ''')
    emprestimos = cur.fetchall()
    if emprestimos:
        for e in emprestimos:
            print(f"ID: {e[0]}, Usuário: {e[1]}, Livro: {e[2]}, Empréstimo: {e[3]}, Previsto: {e[4]}, Devolvido: {e[5]}")
    else:
        print("Nenhum empréstimo registrado.")
    con.close()

def devolver_livro():
    try:
        id_emprestimo = int(input("ID do empréstimo: "))
        data_devolucao = datetime.now().strftime("%Y-%m-%d")

        con = conectar()
        cur = con.cursor()

        # Recuperar o ID do livro associado ao empréstimo
        cur.execute("SELECT id_livro FROM Emprestimo WHERE id = ?", (id_emprestimo,))
        resultado = cur.fetchone()
        if not resultado:
            print("Empréstimo não encontrado.")
            return
        id_livro = resultado[0]

        # Atualiza a devolução e a quantidade de livros
        cur.execute("UPDATE Emprestimo SET data_devolucao = ? WHERE id = ?",
                    (data_devolucao, id_emprestimo))
        cur.execute("UPDATE Livro SET quantidade = quantidade + 1 WHERE id = ?", (id_livro,))

        con.commit()
        print("Livro devolvido com sucesso!")
    except Exception as e:
        print("Erro ao registrar devolução:", e)
    finally:
        con.close()
#--------------------------------------------MENU do Usuario---------------------------------------------------------
def menu():
    criar_tabelas()
    while True:
        print("\n--- Menu Biblioteca ---")
        print("1. Adicionar Livro")
        print("2. Listar Livros")
        print("3. Atualizar Quantidade de Livro")
        print("4. Deletar Livro")
        print("5. Cadastrar Usuário")
        print("6. Listar Usuários")
        print("7. Atualizar Usuário")
        print("8. Deletar Usuário")
        print("9. Registrar Empréstimo")
        print("10. Listar Empréstimos")
        print("11. Devolver Livro")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_livro()
        elif opcao == "2":
            listar_livros()
        elif opcao == "3":
            atualizar_livro()
        elif opcao == "4":
            deletar_livro()
        elif opcao == "5":
            adicionar_usuario()
        elif opcao == "6":
            listar_usuarios()
        elif opcao == "7":
            atualizar_usuario()
        elif opcao == "8":
            deletar_usuario()
        elif opcao == "9":
            registrar_emprestimo()
        elif opcao == "10":
            listar_emprestimos()
        elif opcao == "11":
            devolver_livro()

        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
