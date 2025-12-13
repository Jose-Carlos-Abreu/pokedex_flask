# 🔴 Pokédex Flask ⚪

Este é um projeto web desenvolvido com Flask que simula uma Pokédex, buscando dados de Pokémons através da [PokeAPI](https://pokeapi.co/). O projeto inclui funcionalidades completas de autenticação de usuários (Cadastro, Login, Logout) usando Flask-Login e persistência de dados via SQLite/SQLAlchemy.

## 📸 Visão Geral do Projeto

Abaixo estão alguns screenshots que ilustram o layout unificado e as funcionalidades do aplicativo.

### 1. Página Principal (Catálogo)

O catálogo exibe os Pokémons paginados e a barra de busca, mantendo o header de navegação (Login/Logout) no topo.

![Screenshot da Página Principal da Pokédex](URL_DA_IMAGEM_DA_PAGINA_HOME)

### 2. Formulário de Autenticação (Login)

Usando Herança de Templates, os formulários de Login e Cadastro aparecem mantendo o cabeçalho e a estrutura visual da Pokédex.

![Screenshot da Tela de Login](URL_DA_IMAGEM_DA_PAGINA_DE_LOGIN)

## 🚀 Funcionalidades

* **Catálogo Principal:** Exibe uma lista de Pokémons com paginação, obtidos da PokeAPI.
* **Busca:** Permite buscar Pokémons específicos por nome.
* **Autenticação Segura:**
    * Cadastro de novos usuários com senha criptografada (Hashing).
    * Login/Logout e controle de sessão.
    * Rotas protegidas (como as de edição/exclusão de conta).
* **Layout Unificado:** Utiliza o padrão de Herança de Templates (Jinja2) para manter o cabeçalho e a navegação da Pokédex em todas as páginas.

## 📋 Pré-requisitos

Para rodar este projeto, você precisará ter o **Python 3** instalado em sua máquina.

## 🛠️ Configuração e Instalação

Siga os passos abaixo para configurar e rodar o projeto localmente.

### 1. Clonar o Repositório

```bash
git clone [https://docs.github.com/pt/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github](https://docs.github.com/pt/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
cd [NOME-DO-SEU-PROJETO]

🤝 Contribuições
Sinta-se à vontade para sugerir melhorias, corrigir bugs ou adicionar novas funcionalidades.