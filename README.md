
# Trabalho 1 - LTP2 - CRUD e SQL

Trabalho de Python que gerencia dados de uma bliblioteca utilizando um banco de dados SQLite.


## Autores

- Felipe Rios dos Santos - RA: 22403886

- Ana Luisa Rigotti Leite - RA: 22400558

- Arthur Torquato Novais - RA: 22508414 (Pkmn favorito: Luxray)(Cor favorita: Verde)(Comida favorita: escondidinho de carne)

## Testes feitos

  [Link da documentação](https://docs.google.com/document/d/1zQ6hmow7jbYcGcc9DAYuJLumh8l8INPJvv7pkLTEhR8/edit?usp=sharing)


## Funcionamento do código

####  1 - Banco de Dados

- É criado automaticamente com tabelas: Livro, Usuario, Emprestimo (e
Funcionario.
- Cada tabela tem colunas como id, nome, quantidade, cpf, etc.

####   2 - Funções CRUD (para cada tabela)

- Existem funções para *criar*, *ler*, *atualizar* e *deletar* dados nas tabelas
- Por exemplo: 

    -  `adicionar_livro()` cadastra um novo livro.
    -  `listar_livros()` mostra todos os livros.
    -  `atualizar_livro()` muda a quantidade de um livro.
    -  `deletar_livro()` apaga um livro do sistema.
    -  E o mesmo vale para usuários.

####   3 - Empréstimos
- A função `registrar_emprestimo()`:
    -  Recebe o ID do usuário e do livro.
    - Verifica se o livro está disponível.
    - Cadastra o empréstimo e diminui a quantidade de livros disponíveis.


- A função `devolver_livro()`:
    -  Registra a data da devolução.
    - Aumenta a quantidade do livro no estoque.





#### 4 -  Menu interativo
- O usuário escolhe as opções digitando números (ex: 1 para adicionar livro).
- O menu fica rodando até que o usuário escolha sair (opção 0).
- Cada opção chama uma das funções CRUD.
