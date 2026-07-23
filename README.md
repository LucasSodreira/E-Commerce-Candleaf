# 🕯️ Candleaf — E-Commerce de Velas Artesanais

Sistema web de e-commerce desenvolvido com **Django 5** para venda de velas artesanais e aromatizantes.  
O projeto conta com autenticação de usuários, cadastro e gerenciamento de produtos, busca por nome e painel administrativo.

---

## Funcionalidades

- **Catálogo de produtos** — Listagem com busca por nome e filtro por categoria
- **Detalhe do produto** — Página individual com descrição, preço e imagem
- **Cadastro de usuário** — Novos usuários são automaticamente associados ao grupo *CLIENTE*
- **Login / Logout** — Autenticação com grupos de permissão (*ADMINISTRADOR* e *CLIENTE*)
- **CRUD de produtos** — Criar, editar e remover produtos (restrito a administradores)
- **Painel admin** — Gerenciamento completo via `/admin/`
- **Busca AJAX** — Filtro de produtos sem recarregar a página

---

## Tecnologias

| Ferramenta | Versão |
|------------|--------|
| Python     | 3.11+  |
| Django     | 5.0    |
| SQLite     | 3.x    |
| Pillow     | 10.x   |
| psycopg2   | 2.9    |

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
pip install django pillow
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
├── core/                    # Aplicativo principal
│   ├── management/commands/ # Comandos personalizados (load_db_data)
│   ├── migrations/          # Migrações do banco de dados
│   ├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   │   ├── css/
│   │   ├── img/
│   │   └── js/
│   ├── templates/           # Templates HTML
│   ├── admin.py             # Configuração do painel admin
│   ├── decorators.py        # Decorator de permissão por grupo
│   ├── forms.py             # Formulários (ProdutoForm, UserCreateForm)
│   ├── models.py            # Modelos (User, Categoria, Produto)
│   ├── tests.py             # Testes automatizados
│   └── views.py             # Views (lógica das páginas)
├── e_commerce/              # Configurações do projeto Django
│   ├── settings.py          # Configurações gerais
│   └── urls.py              # Mapeamento de URLs
├── media/                   # Uploads de usuários (imagens)
├── manage.py                # Utilitário de linha de comando
└── README.md
```

---

## Testes

O projeto possui **55 testes automatizados** divididos em 6 classes de teste.

### Como executar

```bash
python manage.py test core
```

Para mais detalhes (verbosidade):

```bash
python manage.py test core --verbosity=2
```

### O que os testes cobrem

#### Testes Unitários (Modelos)

| Classe | Testes | Descrição |
|--------|--------|-----------|
| `UserModelTest` | 3 | Criação de usuário, superusuário, representação `__str__` |
| `CategoriaModelTest` | 2 | Criação de categoria, `__str__` |
| `ProdutoModelTest` | 8 | Criação com/sem imagem, relacionamentos FK, `__str__`, deleção em cascata |

#### Testes Unitários (Formulários)

| Classe | Testes | Descrição |
|--------|--------|-----------|
| `ProdutoFormTest` | 5 | Form válido, campos obrigatórios, widgets, validação de tipos |

#### Testes Unitários (Decorators)

| Classe | Testes | Descrição |
|--------|--------|-----------|
| `DecoratorsTest` | 4 | Acesso permitido/negado por grupo, ausência de autenticação |

#### Testes de Sistema (Views + URLs)

| Classe | Testes | Descrição |
|--------|--------|-----------|
| `ViewsTest` | 27 | Status HTTP, templates usados, contexto das views, fluxo de criação/edição/remoção de produtos, cadastro/login/logout, busca por nome, requisição AJAX |
| `URLsTest` | 6 | Resolução de URLs, reversão de nomes, parâmetros dinâmicos |

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
