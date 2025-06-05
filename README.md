# Sistema de Vendas Online com Django

Este projeto é um sistema de vendas online completo desenvolvido em Django, um framework web Python de alto nível. Ele foi projetado para demonstrar os fundamentos do desenvolvimento web com Django, incluindo CRUD (Criação, Leitura, Atualização e Exclusão) de produtos e usuários, autenticação, controle de sessão, integração com APIs externas e visualização de dados através de gráficos.

## Funcionalidades Principais

* **CRUD de Produtos:** Gerenciamento completo de produtos (cadastro, listagem, edição, exclusão).
* **Integração de API:** Exibição de produtos de uma API externa (Fakestore API) para complementar o catálogo.
* **CRUD de Usuários:** Cadastro, listagem, edição e exclusão de usuários.
* **Autenticação e Controle de Sessão:** Sistema robusto de login/logout com controle de acesso a páginas restritas.
* **Preenchimento Automático de Endereço:** Integração com a API ViaCEP para preenchimento automático de campos de endereço no cadastro de usuário.
* **Funcionalidade de Compra:** Processo de checkout para produtos, incluindo registro de vendas.
* **Dashboard Administrativo:** Painel de controle com acesso a funcionalidades chave.
* **Relatórios Visuais:** Gráficos de estoque de produtos e de vendas por dia.
* **Design Moderno e Responsivo:** Interface de usuário minimalista e elegante, otimizada para diferentes tamanhos de tela.

## Tecnologias Utilizadas

* **Backend:** Python, Django
* **Frontend:** HTML, CSS (design responsivo)
* **Banco de Dados:** SQLite (padrão Django, configurável para outros DBs)
* **APIs Externas:** ViaCEP, Fakestore API
* **Visualização de Dados:** Matplotlib

## Como Rodar o Projeto Localmente

Siga estas instruções para configurar e executar o projeto na sua máquina local.

### Pré-requisitos

* Python 3.x instalado.
* `pip` (gerenciador de pacotes do Python).

### Passos

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/SeuUsuario/SeuRepositorio.git](https://github.com/SeuUsuario/SeuRepositorio.git)
    cd SeuRepositorio
    ```
    *(Substitua `SeuUsuario` e `SeuRepositorio` pelo caminho real do seu projeto no GitHub)*

2.  **Crie e Ative um Ambiente Virtual:**
    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python -m venv ambienteVirtual
    # No Windows:
    .\ambienteVirtual\Scripts\activate
    # No macOS/Linux:
    source ambienteVirtual/bin/activate
    ```

3.  **Instale as Dependências:**
    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias.
    ```bash
    pip install django requests matplotlib Pillow
    ```

4.  **Configure o Banco de Dados e Crie Migrações:**
    Aplique as migrações para criar as tabelas do banco de dados.
    ```bash
    python manage.py makemigrations app
    python manage.py migrate
    ```

5.  **Crie um Superusuário (Opcional, mas Recomendado):**
    Para acessar o painel de administração do Django e gerenciar dados.
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções no terminal para criar o nome de usuário e a senha.

6.  **Execute o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

7.  **Acesse o Projeto:**
    Abra seu navegador e vá para `http://127.0.0.1:8000/`.

    Você pode acessar o painel de administração em `http://127.0.0.1:8000/admin/` com as credenciais do superusuário.

## Estrutura do Projeto

* `projeto/`: Configurações principais do Django.
* `app/`: Aplicação principal do sistema.
    * `models.py`: Definições dos modelos de dados (Usuário, Produto, Venda, Categoria).
    * `views.py`: Lógica de negócio e funções de visualização.
    * `forms.py`: Definições dos formulários HTML.
    * `urls.py`: Mapeamento das URLs para as views.
    * `templates/`: Ficheiros HTML para a interface do usuário.
    * `static/`: Ficheiros CSS e outros recursos estáticos.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença

Este projeto está licenciado sob a licença MIT.

---
