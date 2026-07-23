import pytest
from django.urls import reverse, resolve
from core.models import User, Categoria, Produto
from core.forms import ProdutoForm


# =============================================================================
# Testes do modelo User
# =============================================================================

@pytest.mark.django_db
class TestUserModel:

    def test_criacao_usuario(self):
        """Verifica se um usuário é criado corretamente."""
        user = User.objects.create_user(
            username='testeuser', password='senha123', email='teste@email.com'
        )
        assert user.username == 'testeuser'
        assert user.email == 'teste@email.com'
        assert user.check_password('senha123')

    def test_str_usuario(self):
        """Verifica a representação em string do usuário."""
        user = User.objects.create_user(username='testeuser', password='senha123')
        assert str(user) == 'testeuser'

    def test_usuario_superuser(self):
        """Verifica a criação de um superusuário."""
        admin = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@email.com'
        )
        assert admin.is_superuser
        assert admin.is_staff


# =============================================================================
# Testes do modelo Categoria
# =============================================================================

@pytest.mark.django_db
class TestCategoriaModel:

    def test_criacao_categoria(self, categoria):
        """Verifica se uma categoria é criada corretamente."""
        assert categoria.nome == 'Velas'

    def test_str_categoria(self, categoria):
        """Verifica a representação em string da categoria."""
        assert str(categoria) == 'Velas'


# =============================================================================
# Testes do modelo Produto
# =============================================================================

@pytest.mark.django_db
class TestProdutoModel:

    def test_criacao_produto(self, usuario_admin, categoria):
        """Verifica se um produto é criado corretamente com todos os campos."""
        produto = Produto.objects.create(
            nome='Vela Lavanda',
            descricao='Vela artesanal com aroma de lavanda',
            preco=29.90,
            categoria=categoria,
            user=usuario_admin,
        )
        assert produto.nome == 'Vela Lavanda'
        assert produto.descricao == 'Vela artesanal com aroma de lavanda'
        assert float(produto.preco) == 29.90
        assert produto.categoria == categoria
        assert produto.user == usuario_admin

    def test_str_produto(self, usuario_admin, categoria):
        """Verifica a representação em string do produto."""
        produto = Produto.objects.create(
            nome='Vela Baunilha', descricao='Vela de baunilha',
            preco=35.00, categoria=categoria, user=usuario_admin,
        )
        assert str(produto) == 'Vela Baunilha'

    def test_produto_com_imagem(self, usuario_admin, categoria, imagem_teste):
        """Verifica se um produto pode ser criado com imagem."""
        produto = Produto.objects.create(
            nome='Vela Rosa', descricao='Vela rosa',
            preco=45.00, categoria=categoria, user=usuario_admin,
            imagem=imagem_teste,
        )
        assert produto.imagem is not None
        assert produto.imagem.name.startswith('produtos/')

    def test_produto_sem_imagem(self, usuario_admin, categoria):
        """Verifica se um produto pode ser criado sem imagem."""
        produto = Produto.objects.create(
            nome='Vela Sem Imagem', descricao='Vela sem foto',
            preco=15.00, categoria=categoria, user=usuario_admin,
        )
        assert not produto.imagem

    def test_relacionamento_produto_categoria(self, usuario_admin, categoria):
        """Verifica o relacionamento ForeignKey entre Produto e Categoria."""
        produto = Produto.objects.create(
            nome='Difusor', descricao='Difusor de aromas',
            preco=59.90, categoria=categoria, user=usuario_admin,
        )
        assert produto.categoria.nome == 'Velas'

    def test_relacionamento_produto_user(self, usuario_admin, categoria):
        """Verifica o relacionamento ForeignKey entre Produto e User."""
        produto = Produto.objects.create(
            nome='Sabonete', descricao='Sabonete artesanal',
            preco=12.50, categoria=categoria, user=usuario_admin,
        )
        assert produto.user.username == 'admin'

    def test_delete_cascade_categoria(self, usuario_admin, categoria):
        """Verifica se ao deletar uma categoria, os produtos são deletados."""
        Produto.objects.create(
            nome='Vela Canela', descricao='Vela de canela',
            preco=25.00, categoria=categoria, user=usuario_admin,
        )
        categoria.delete()
        assert Produto.objects.filter(categoria__isnull=False).count() == 0


# =============================================================================
# Testes do ProdutoForm
# =============================================================================

@pytest.mark.django_db
class TestProdutoForm:

    def test_form_valido(self, categoria):
        """Verifica se o formulário é válido com dados corretos."""
        dados = {'nome': 'Vela Teste', 'descricao': 'Descrição',
                 'preco': '39.90', 'categoria': categoria.pk}
        form = ProdutoForm(data=dados)
        assert form.is_valid()

    def test_form_invalido_sem_nome(self, categoria):
        """Verifica se o formulário é inválido sem o campo nome."""
        dados = {'descricao': 'Descrição', 'preco': '39.90',
                 'categoria': categoria.pk}
        form = ProdutoForm(data=dados)
        assert not form.is_valid()
        assert 'nome' in form.errors

    def test_form_invalido_preco_invalido(self, categoria):
        """Verifica se o formulário rejeita preço com texto."""
        dados = {'nome': 'Vela Teste', 'descricao': 'Descrição',
                 'preco': 'abc', 'categoria': categoria.pk}
        form = ProdutoForm(data=dados)
        assert not form.is_valid()

    def test_form_campos_presentes(self):
        """Verifica se os campos esperados estão no formulário."""
        form = ProdutoForm()
        campos_esperados = {'nome', 'descricao', 'preco', 'categoria', 'imagem'}
        assert set(form.fields.keys()) == campos_esperados

    def test_form_widgets(self):
        """Verifica se os widgets possuem os atributos corretos."""
        form = ProdutoForm()
        assert form.fields['nome'].widget.attrs['placeholder'] == 'Informe o título do produto'
        assert form.fields['preco'].widget.attrs['step'] == '0.01'


# =============================================================================
# Testes do decorator group_required
# =============================================================================

class TestDecorators:

    @pytest.mark.django_db
    def test_usuario_autenticado_grupo_correto(self, client, usuario_admin):
        """Verifica se usuário autenticado no grupo certo tem acesso."""
        client.force_login(usuario_admin)
        response = client.get(reverse('cadastro_produto'))
        assert response.status_code != 403

    @pytest.mark.django_db
    def test_usuario_autenticado_grupo_errado(self, client, usuario_cliente):
        """Verifica se usuário autenticado no grupo errado recebe 403."""
        client.force_login(usuario_cliente)
        response = client.get(reverse('cadastro_produto'))
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_usuario_nao_autenticado(self, client):
        """Verifica se usuário não autenticado recebe 403."""
        response = client.get(reverse('cadastro_produto'))
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_usuario_sem_grupo(self, client, usuario_sem_grupo):
        """Verifica se usuário sem grupo recebe 403."""
        client.force_login(usuario_sem_grupo)
        response = client.get(reverse('cadastro_produto'))
        assert response.status_code == 403


# =============================================================================
# Testes de Views (sistema)
# =============================================================================

@pytest.mark.django_db
class TestViewsListarProdutos:

    def test_index_status_code(self, client, produto):
        """Verifica se a página inicial retorna status 200."""
        response = client.get(reverse('index'))
        assert response.status_code == 200

    def test_index_contexto_produtos(self, client, produto):
        """Verifica se o contexto contém produtos."""
        response = client.get(reverse('index'))
        assert 'produtos' in response.context
        assert produto in response.context['produtos']

    def test_index_contexto_categorias(self, client, produto, categoria):
        """Verifica se o contexto contém categorias."""
        response = client.get(reverse('index'))
        assert 'categorias' in response.context
        assert categoria in response.context['categorias']

    def test_index_busca_por_nome(self, client, usuario_admin, categoria):
        """Verifica a busca de produtos pelo nome."""
        Produto.objects.create(
            nome='Vela Lavanda', descricao='Teste', preco=30.00,
            categoria=categoria, user=usuario_admin,
        )
        response = client.get(reverse('index'), {'nome_produto': 'Lavanda'})
        assert response.status_code == 200
        assert 'Vela Lavanda' in response.content.decode()

    def test_index_ajax_request(self, client, produto):
        """Verifica se requisição AJAX retorna o partial."""
        response = client.get(
            reverse('index'), {'nome_produto': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        assert response.status_code == 200


class TestViewsPagProduct:

    @pytest.mark.django_db
    def test_pag_product_status_code(self, client, produto):
        """Verifica se a página de detalhe retorna 200."""
        response = client.get(reverse('pag_product', args=[produto.id]))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_pag_product_contexto(self, client, produto):
        """Verifica se o contexto contém o produto correto."""
        response = client.get(reverse('pag_product', args=[produto.id]))
        assert response.context['produto'] == produto

    @pytest.mark.django_db
    def test_pag_product_404(self, client):
        """Verifica se um ID inexistente retorna 404."""
        response = client.get(reverse('pag_product', args=[9999]))
        assert response.status_code == 404


class TestViewsProdutoCriar:

    @pytest.mark.django_db
    def test_get_autenticado(self, client, usuario_admin, categoria):
        """Verifica se admin autenticado acessa o formulário de criação."""
        client.force_login(usuario_admin)
        response = client.get(reverse('cadastro_produto'))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_post_valido(self, client, usuario_admin, categoria):
        """Verifica se um produto é criado via POST com dados válidos."""
        client.force_login(usuario_admin)
        dados = {'nome': 'Novo Produto Teste', 'descricao': 'Descrição',
                 'preco': '99.90', 'categoria': categoria.pk}
        response = client.post(reverse('cadastro_produto'), dados, follow=True)
        assert response.status_code == 200
        assert Produto.objects.filter(nome='Novo Produto Teste').exists()

    @pytest.mark.django_db
    def test_post_sem_autenticacao(self, client, categoria):
        """Verifica que usuário não autenticado recebe 403."""
        dados = {'nome': 'Produto Sem Auth', 'descricao': 'Teste',
                 'preco': '10.00', 'categoria': categoria.pk}
        response = client.post(reverse('cadastro_produto'), dados)
        assert response.status_code == 403


class TestViewsProdutoEditar:

    @pytest.mark.django_db
    def test_get_autenticado(self, client, usuario_admin, produto):
        """Verifica se admin autenticado acessa o formulário de edição."""
        client.force_login(usuario_admin)
        response = client.get(reverse('produto_editar', args=[produto.id]))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_post_valido(self, client, usuario_admin, produto, categoria):
        """Verifica se um produto é atualizado via POST."""
        client.force_login(usuario_admin)
        dados = {'nome': 'Vela Editada', 'descricao': 'Descrição editada',
                 'preco': '149.90', 'categoria': categoria.pk}
        response = client.post(
            reverse('produto_editar', args=[produto.id]), dados, follow=True
        )
        assert response.status_code == 200
        produto.refresh_from_db()
        assert produto.nome == 'Vela Editada'
        assert float(produto.preco) == 149.90


class TestViewsProdutoRemover:

    @pytest.mark.django_db
    def test_remover_autenticado(self, client, usuario_admin, produto):
        """Verifica se admin autenticado pode remover um produto."""
        client.force_login(usuario_admin)
        response = client.post(
            reverse('produto_remover', args=[produto.id]), follow=True
        )
        assert response.status_code == 200
        assert not Produto.objects.filter(id=produto.id).exists()

    @pytest.mark.django_db
    def test_remover_nao_autenticado(self, client, produto):
        """Verifica que não autenticado recebe 403 ao remover."""
        response = client.get(reverse('produto_remover', args=[produto.id]))
        assert response.status_code == 403


@pytest.mark.django_db
class TestViewsLogin:

    def test_login_get(self, client):
        """Verifica se a página de login retorna 200."""
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_login_post_valido(self, client, usuario_admin):
        """Verifica se o login funciona com credenciais corretas."""
        response = client.post(reverse('login'), {
            'username': 'admin', 'password': 'admin123',
        }, follow=True)
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse('index')

    def test_login_post_invalido(self, client):
        """Verifica se o login falha com credenciais incorretas."""
        response = client.post(reverse('login'), {
            'username': 'admin', 'password': 'senha_errada',
        })
        assert response.status_code == 200
        assert 'Credenciais inválidas' in response.content.decode()

    def test_login_redireciona_se_autenticado(self, client, usuario_admin):
        """Verifica se usuário logado é redirecionado para o index."""
        client.force_login(usuario_admin)
        response = client.get(reverse('login'))
        assert response.status_code == 302
        assert response.url == reverse('index')


@pytest.mark.django_db
class TestViewsCadastro:

    def test_cadastro_get(self, client):
        """Verifica se a página de cadastro retorna 200."""
        response = client.get(reverse('cadastro'))
        assert response.status_code == 200

    def test_cadastro_post_valido(self, client, grupo_cliente):
        """Verifica se um novo usuário é cadastrado com sucesso."""
        response = client.post(reverse('cadastro'), {
            'username': 'novousuario',
            'password1': 'senhaForte123!',
            'password2': 'senhaForte123!',
        }, follow=True)
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse('login')
        assert User.objects.filter(username='novousuario').exists()

    def test_cadastro_usuario_grupo_cliente(self, client, grupo_cliente):
        """Verifica se o novo usuário é associado ao grupo CLIENTE."""
        client.post(reverse('cadastro'), {
            'username': 'novocliente',
            'password1': 'senhaForte123!',
            'password2': 'senhaForte123!',
        })
        usuario = User.objects.get(username='novocliente')
        assert usuario.groups.filter(name='CLIENTE').exists()

    def test_cadastro_redireciona_se_autenticado(self, client, usuario_admin):
        """Verifica se usuário logado é redirecionado para o index."""
        client.force_login(usuario_admin)
        response = client.get(reverse('cadastro'))
        assert response.status_code == 302
        assert response.url == reverse('index')


@pytest.mark.django_db
class TestViewsDesconectar:

    def test_desconectar(self, client, usuario_admin):
        """Verifica se o logout funciona e redireciona para o index."""
        client.force_login(usuario_admin)
        response = client.get(reverse('desconectar'), follow=True)
        assert response.status_code == 200
        assert response.redirect_chain[-1][0] == reverse('index')
        # Verifica que o usuário não está mais autenticado
        response = client.get(reverse('index'))
        assert not response.context['user'].is_authenticated


# =============================================================================
# Testes de URLs
# =============================================================================

class TestURLs:

    def test_url_index_resolve(self):
        """Verifica se a URL '/' resolve para a view correta."""
        resolver = resolve('/')
        assert resolver.func.__name__ == 'listar_produtos'
        assert resolver.url_name == 'index'

    def test_url_login_resolve(self):
        resolver = resolve('/login/')
        assert resolver.func.__name__ == 'login'

    def test_url_cadastro_resolve(self):
        resolver = resolve('/cadastro/')
        assert resolver.func.__name__ == 'cadastro'

    def test_url_desconectar_resolve(self):
        resolver = resolve('/desconectar/')
        assert resolver.func.__name__ == 'desconectar'

    def test_url_produto_criar_resolve(self):
        resolver = resolve('/cadastro_produto/')
        assert resolver.func.__name__ == 'produto_criar'

    def test_url_admin_resolve(self):
        resolver = resolve('/admin/')
        assert resolver.func.__name__ == 'index'

    def test_urls_com_id_resolvem(self):
        resolver_produto = resolve('/produto/1/')
        assert resolver_produto.func.__name__ == 'pag_product'
        resolver_editar = resolve('/produto/editar/1/')
        assert resolver_editar.func.__name__ == 'produto_editar'
        resolver_remover = resolve('/produto/remover/1/')
        assert resolver_remover.func.__name__ == 'produto_remover'

    def test_urls_reverse(self):
        assert reverse('index') == '/'
        assert reverse('login') == '/login/'
        assert reverse('cadastro') == '/cadastro/'
        assert reverse('desconectar') == '/desconectar/'
        assert reverse('cadastro_produto') == '/cadastro_produto/'
        assert reverse('pag_product', args=[1]) == '/produto/1/'
        assert reverse('produto_editar', args=[1]) == '/produto/editar/1/'
        assert reverse('produto_remover', args=[1]) == '/produto/remover/1/'
