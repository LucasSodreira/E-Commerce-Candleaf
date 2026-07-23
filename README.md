# 🕯️ Candleaf — E-Commerce de Velas Artesanais

Sistema web de e-commerce desenvolvido com **Django 5** para venda de velas artesanais e aromatizantes.
O projeto conta com autenticação de usuários, cadastro e gerenciamento de produtos, busca por nome e painel administrativo.

---

## Funcionalidades

- **Catálogo de produtos** — Listagem com busca por nome
- **Detalhe do produto** — Página individual com descrição, preço e imagem
- **Cadastro de usuário** — Novos usuários são automaticamente associados ao grupo *CLIENTE*
- **Login / Logout** — Autenticação com grupos de permissão (*ADMINISTRADOR* e *CLIENTE*)
- **CRUD de produtos** — Criar, editar e remover produtos (restrito a administradores)
- **Painel admin** — Gerenciamento completo via `/admin/`
- **Busca AJAX** — Filtro de produtos sem recarregar a página

---

## Tecnologias

| Ferramenta | Versão  |
|------------|---------|
| Python     | 3.11+   |
| Django     | 5.0     |
| SQLite     | 3.x     |
| Pillow     | 10.x    |
| pytest     | 7.4+    |
| pytest-django | 4.7+ |

---

## Como Rodar

### 1. Clone o repositório e entre na pasta

```bash
cd e_commerce
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install django pillow pytest pytest-django
```

### 4. Execute as migrações

```bash
python manage.py migrate
```

### 5. (Opcional) Carregue dados iniciais

Cria os grupos *ADMINISTRADOR* e *CLIENTE*:

```bash
python manage.py load_db_data
```

### 6. (Opcional) Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor

```bash
python manage.py runserver
```

Acesse [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Estrutura do Projeto

```
e_commerce/
├── conftest.py               # Fixtures compartilhadas do pytest
├── pytest.ini                # Configuração do pytest-django
├── core/                     # Aplicativo principal
│   ├── management/commands/  # Comandos personalizados (load_db_data)
│   ├── migrations/           # Migrações do banco de dados
│   ├── static/               # Arquivos estáticos (CSS, JS, imagens)
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   ├── templates/            # Templates HTML
│   ├── admin.py              # Configuração do painel admin
│   ├── decorators.py         # Decorator de permissão por grupo
│   ├── forms.py              # Formulários (ProdutoForm, UserCreateForm)
│   ├── models.py             # Modelos (User, Categoria, Produto)
│   ├── tests.py              # Testes com pytest-django
│   └── views.py              # Views (lógica das páginas)
├── e_commerce/               # Configurações do projeto Django
│   ├── settings.py           # Configurações gerais
│   └── urls.py               # Mapeamento de URLs
├── media/                    # Uploads de usuários (imagens)
├── manage.py                 # Utilitário de linha de comando
└── README.md
```

---

## Testes

O projeto possui **53 testes automatizados** com **pytest** + **pytest-django**,
distribuídos em 13 classes de teste.

### Como executar

```bash
pytest
```

Com relatório detalhado:

```bash
pytest -v
```

Para rodar apenas um arquivo ou classe:

```bash
pytest core/tests.py
pytest core/tests.py::TestProdutoModel
pytest core/tests.py::TestViewsLogin::test_login_post_valido
```

### O que os testes cobrem

#### Modelos (`TestUserModel`, `TestCategoriaModel`, `TestProdutoModel`)

| Teste | Descrição |
|-------|-----------|
| `test_criacao_usuario` | Criação de usuário com username, email e senha |
| `test_usuario_superuser` | Criação de superusuário (is_superuser, is_staff) |
| `test_criacao_produto` | Criação de produto com todos os campos e relacionamentos |
| `test_produto_com_imagem` | Upload de imagem no produto |
| `test_produto_sem_imagem` | Produto pode ser criado sem imagem |
| `test_delete_cascade_categoria` | Deleção em cascata ao remover categoria |
| `test_relacionamento_produto_categoria` | FK Produto → Categoria |
| `test_relacionamento_produto_user` | FK Produto → User |
| `test_str_*` | Representação `__str__` de todos os modelos |

#### Formulários (`TestProdutoForm`)

| Teste | Descrição |
|-------|-----------|
| `test_form_valido` | Formulário aceita dados corretos |
| `test_form_invalido_sem_nome` | Validação de campo obrigatório |
| `test_form_invalido_preco_invalido` | Validação de tipo do campo preço |
| `test_form_campos_presentes` | Verifica os campos do formulário |
| `test_form_widgets` | Verifica atributos dos widgets (placeholder, step) |

#### Decorator de Permissão (`TestDecorators`)

| Teste | Descrição |
|-------|-----------|
| `test_usuario_autenticado_grupo_correto` | Admin acessa páginas restritas (status ≠ 403) |
| `test_usuario_autenticado_grupo_errado` | Cliente recebe 403 em páginas de admin |
| `test_usuario_nao_autenticado` | Anônimo recebe 403 |
| `test_usuario_sem_grupo` | Usuário sem grupo recebe 403 |

#### Views — Funcionalidades (`TestViews*`)

| Teste | Descrição |
|-------|-----------|
| `test_index_status_code` | Página inicial retorna 200 |
| `test_index_busca_por_nome` | Busca de produtos pelo nome |
| `test_index_ajax_request` | Requisição AJAX retorna conteúdo parcial |
| `test_pag_product_status_code` | Página de detalhe retorna 200 |
| `test_pag_product_404` | ID inexistente retorna 404 |
| `test_produto_criar_post_valido` | Criação de produto via POST |
| `test_produto_criar_post_sem_autenticacao` | Bloqueio de criação para não autenticados |
| `test_produto_editar_post_valido` | Atualização de produto via POST |
| `test_produto_remover_autenticado` | Remoção de produto por admin |
| `test_produto_remover_nao_autenticado` | Bloqueio de remoção para não autenticados |
| `test_login_post_valido` | Login com credenciais corretas |
| `test_login_post_invalido` | Login com credenciais incorretas |
| `test_login_redireciona_se_autenticado` | Redirecionamento de usuário já logado |
| `test_cadastro_post_valido` | Cadastro de novo usuário |
| `test_cadastro_usuario_grupo_cliente` | Associação automática ao grupo CLIENTE |
| `test_desconectar` | Logout e verificação de sessão encerrada |

#### URLs (`TestURLs`)

| Teste | Descrição |
|-------|-----------|
| `test_url_*_resolve` | Cada URL resolve para a view correta |
| `test_urls_com_id_resolvem` | URLs com parâmetro dinâmico funcionam |
| `test_urls_reverse` | Nomes das URLs geram os caminhos corretos |

### Fluxos testados

- ✅ Usuário não autenticado **não** consegue criar/editar/remover produtos (403)
- ✅ Apenas administradores podem acessar CRUD de produtos
- ✅ Clientes **não** conseguem acessar páginas restritas
- ✅ Cadastro de novo usuário com associação automática ao grupo *CLIENTE*
- ✅ Login com credenciais válidas e inválidas
- ✅ Redirecionamento de usuários já logados
- ✅ Logout e verificação de sessão encerrada
- ✅ Busca de produtos por nome (case-insensitive)
- ✅ Requisição AJAX retorna template parcial
- ✅ Páginas de produto inexistente retornam 404
- ✅ Deleção em cascata de produtos ao remover categoria

---

## Modelos de Dados

```python
User(AbstractUser)           # Usuário personalizado
├── groups                   # M2M → Group (related_name='core_users')
└── user_permissions         # M2M → Permission

Categoria
└── nome: str                # Ex: "Velas", "Aromatizantes"

Produto
├── nome: str                # Nome do produto
├── descricao: text          # Descrição detalhada
├── preco: Decimal           # Preço (8 dígitos, 2 casas decimais)
├── categoria: FK → Categoria
├── imagem: ImageField       # Upload para /produtos/
└── user: FK → User          # Quem cadastrou o produto
```

---

## Licença

Projeto desenvolvido para fins de estudo.
