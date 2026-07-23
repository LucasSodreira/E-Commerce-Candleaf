import tempfile
from io import BytesIO
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden
from .models import User, Categoria, Produto
from .forms import ProdutoForm
from .decorators import group_required


def criar_imagem_teste():
    """Cria uma imagem PNG em memória para usar nos testes."""
    img = Image.new('RGB', (100, 100), color='red')
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return SimpleUploadedFile('teste.png', buf.read(), content_type='image/png')


class UserModelTest(TestCase):
    """Testes unitários para o modelo User."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testeuser',
            password='senha123',
            email='teste@email.com'
        )

    def test_criacao_usuario(self):
        """Verifica se um usuário é criado corretamente."""
        self.assertEqual(self.user.username, 'testeuser')
        self.assertEqual(self.user.email, 'teste@email.com')
        self.assertTrue(self.user.check_password('senha123'))

    def test_str_usuario(self):
        """Verifica a representação em string do usuário."""
        self.assertEqual(str(self.user), 'testeuser')

    def test_usuario_superuser(self):
        """Verifica a criação de um superusuário."""
        admin = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@email.com'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


class CategoriaModelTest(TestCase):
    """Testes unitários para o modelo Categoria."""

    def setUp(self):
        self.categoria = Categoria.objects.create(nome='Velas')

    def test_criacao_categoria(self):
        """Verifica se uma categoria é criada corretamente."""
        self.assertEqual(self.categoria.nome, 'Velas')

    def test_str_categoria(self):
        """Verifica a representação em string da categoria."""
        self.assertEqual(str(self.categoria), 'Velas')


class ProdutoModelTest(TestCase):
    """Testes unitários para o modelo Produto."""

    def setUp(self):
        self.user = User.objects.create_user(username='vendedor', password='senha123')
        self.categoria = Categoria.objects.create(nome='Aromatizantes')

    def test_criacao_produto(self):
        """Verifica se um produto é criado corretamente com todos os campos."""
        produto = Produto.objects.create(
            nome='Vela Lavanda',
            descricao='Vela artesanal com aroma de lavanda',
            preco=29.90,
            categoria=self.categoria,
            user=self.user,
        )
        self.assertEqual(produto.nome, 'Vela Lavanda')
        self.assertEqual(produto.descricao, 'Vela artesanal com aroma de lavanda')
        self.assertEqual(float(produto.preco), 29.90)
        self.assertEqual(produto.categoria, self.categoria)
        self.assertEqual(produto.user, self.user)

    def test_str_produto(self):
        """Verifica a representação em string do produto."""
        produto = Produto.objects.create(
            nome='Vela Baunilha',
            descricao='Vela com aroma de baunilha',
            preco=35.00,
            categoria=self.categoria,
            user=self.user,
        )
        self.assertEqual(str(produto), 'Vela Baunilha')

    def test_produto_com_imagem(self):
        """Verifica se um produto pode ser criado com imagem."""
        imagem = criar_imagem_teste()
        produto = Produto.objects.create(
            nome='Vela Rosa',
            descricao='Vela rosa',
            preco=45.00,
            categoria=self.categoria,
            user=self.user,
            imagem=imagem,
        )
        self.assertIsNotNone(produto.imagem)
        self.assertTrue(produto.imagem.name.startswith('produtos/'))

    def test_produto_sem_imagem(self):
        """Verifica se um produto pode ser criado sem imagem."""
        produto = Produto.objects.create(
            nome='Vela Sem Imagem',
            descricao='Vela sem foto',
            preco=15.00,
            categoria=self.categoria,
            user=self.user,
        )
        self.assertFalse(produto.imagem)

    def test_relacionamento_produto_categoria(self):
        """Verifica o relacionamento ForeignKey entre Produto e Categoria."""
        produto = Produto.objects.create(
            nome='Difusor',
            descricao='Difusor de aromas',
            preco=59.90,
            categoria=self.categoria,
            user=self.user,
        )
        self.assertEqual(produto.categoria.nome, 'Aromatizantes')

    def test_relacionamento_produto_user(self):
        """Verifica o relacionamento ForeignKey entre Produto e User."""
        produto = Produto.objects.create(
            nome='Sabonete',
            descricao='Sabonete artesanal',
            preco=12.50,
            categoria=self.categoria,
            user=self.user,
        )
        self.assertEqual(produto.user.username, 'vendedor')

    def test_delete_cascade_categoria(self):
        """Verifica se ao deletar uma categoria, os produtos associados também são deletados."""
        Produto.objects.create(
            nome='Vela Canela',
            descricao='Vela de canela',
            preco=25.00,
            categoria=self.categoria,
            user=self.user,
        )
        self.categoria.delete()
        self.assertEqual(Produto.objects.filter(categoria__isnull=False).count(), 0)


class ProdutoFormTest(TestCase):
    """Testes unitários para o ProdutoForm."""

    def setUp(self):
        self.user = User.objects.create_user(username='vendedor', password='senha123')
        self.categoria = Categoria.objects.create(nome='Velas')

    def test_form_valido(self):
        """Verifica se o formulário é válido com dados corretos."""
        dados = {
            'nome': 'Vela Teste',
            'descricao': 'Descrição da vela de teste',
            'preco': '39.90',
            'categoria': self.categoria.pk,
        }
        form = ProdutoForm(data=dados)
        self.assertTrue(form.is_valid())

    def test_form_invalido_sem_nome(self):
        """Verifica se o formulário é inválido sem o campo nome."""
        dados = {
            'descricao': 'Descrição',
            'preco': '39.90',
            'categoria': self.categoria.pk,
        }
        form = ProdutoForm(data=dados)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)

    def test_form_invalido_preco_invalido(self):
        """Verifica se o formulário rejeita preço com texto."""
        dados = {
            'nome': 'Vela Teste',
            'descricao': 'Descrição',
            'preco': 'abc',
            'categoria': self.categoria.pk,
        }
        form = ProdutoForm(data=dados)
        self.assertFalse(form.is_valid())

    def test_form_campos_presentes(self):
        """Verifica se os campos esperados estão no formulário."""
        form = ProdutoForm()
        campos_esperados = {'nome', 'descricao', 'preco', 'categoria', 'imagem'}
        campos_form = set(form.fields.keys())
        self.assertEqual(campos_form, campos_esperados)

    def test_form_widgets(self):
        """Verifica se os widgets possuem os atributos corretos."""
        form = ProdutoForm()
        self.assertEqual(form.fields['nome'].widget.attrs['placeholder'], 'Informe o título do produto')
        self.assertEqual(form.fields['preco'].widget.attrs['step'], '0.01')


class DecoratorsTest(TestCase):
    """Testes unitários para o decorator group_required."""

    def setUp(self):
        self.client = Client()
        self.grupo_admin = Group.objects.create(name='ADMINISTRADOR')
        self.grupo_cliente = Group.objects.create(name='CLIENTE')
        self.user_admin = User.objects.create_user(username='admin', password='admin123')
        self.user_admin.groups.add(self.grupo_admin)
        self.user_cliente = User.objects.create_user(username='cliente', password='cliente123')
        self.user_cliente.groups.add(self.grupo_cliente)
        self.user_sem_grupo = User.objects.create_user(username='solto', password='solto123')

    def test_usuario_autenticado_grupo_correto(self):
        """Verifica se usuário autenticado no grupo certo tem acesso."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('cadastro_produto'))
        self.assertNotEqual(response.status_code, 403)

    def test_usuario_autenticado_grupo_errado(self):
        """Verifica se usuário autenticado no grupo errado recebe 403."""
        self.client.login(username='cliente', password='cliente123')
        response = self.client.get(reverse('cadastro_produto'))
        self.assertEqual(response.status_code, 403)

    def test_usuario_nao_autenticado(self):
        """Verifica se usuário não autenticado recebe 403."""
        response = self.client.get(reverse('cadastro_produto'))
        self.assertEqual(response.status_code, 403)

    def test_usuario_sem_grupo(self):
        """Verifica se usuário sem grupo recebe 403."""
        self.client.login(username='solto', password='solto123')
        response = self.client.get(reverse('cadastro_produto'))
        self.assertEqual(response.status_code, 403)


class ViewsTest(TestCase):
    """Testes de sistema para as views do projeto."""

    def setUp(self):
        self.client = Client()
        self.grupo_admin = Group.objects.create(name='ADMINISTRADOR')
        Group.objects.create(name='CLIENTE')
        self.admin = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@email.com'
        )
        self.admin.groups.add(self.grupo_admin)
        self.user = User.objects.create_user(username='comum', password='comum123')
        self.categoria = Categoria.objects.create(nome='Velas')
        self.produto = Produto.objects.create(
            nome='Vela Teste',
            descricao='Vela de teste automatizado',
            preco=49.90,
            categoria=self.categoria,
            user=self.admin,
        )

    # --- Testes da view listar_produtos (página inicial) ---

    def test_index_status_code(self):
        """Verifica se a página inicial retorna status 200."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_template_usado(self):
        """Verifica se a página inicial usa o template correto."""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'index.html')

    def test_index_contexto_produtos(self):
        """Verifica se o contexto da página inicial contém produtos."""
        response = self.client.get(reverse('index'))
        self.assertIn('produtos', response.context)
        self.assertIn(self.produto, response.context['produtos'])

    def test_index_contexto_categorias(self):
        """Verifica se o contexto da página inicial contém categorias."""
        response = self.client.get(reverse('index'))
        self.assertIn('categorias', response.context)
        self.assertIn(self.categoria, response.context['categorias'])

    def test_index_busca_por_nome(self):
        """Verifica a busca de produtos pelo nome."""
        Produto.objects.create(
            nome='Vela Lavanda', descricao='Teste', preco=30.00,
            categoria=self.categoria, user=self.admin,
        )
        response = self.client.get(reverse('index'), {'nome_produto': 'Lavanda'})
        self.assertContains(response, 'Vela Lavanda')
        self.assertNotContains(response, 'Vela Teste')

    def test_index_ajax_request(self):
        """Verifica se requisição AJAX retorna apenas o partial template."""
        response = self.client.get(
            reverse('index'),
            {'nome_produto': ''},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produtos_parcial.html')

    # --- Testes da view pag_product (detalhe do produto) ---

    def test_pag_product_status_code(self):
        """Verifica se a página de detalhe retorna 200."""
        response = self.client.get(reverse('pag_product', args=[self.produto.id]))
        self.assertEqual(response.status_code, 200)

    def test_pag_product_template_usado(self):
        """Verifica se a página de detalhe usa o template correto."""
        response = self.client.get(reverse('pag_product', args=[self.produto.id]))
        self.assertTemplateUsed(response, 'pag-product.html')

    def test_pag_product_contexto(self):
        """Verifica se o contexto contém o produto correto."""
        response = self.client.get(reverse('pag_product', args=[self.produto.id]))
        self.assertEqual(response.context['produto'], self.produto)

    def test_pag_product_404(self):
        """Verifica se um ID inexistente retorna 404."""
        response = self.client.get(reverse('pag_product', args=[9999]))
        self.assertEqual(response.status_code, 404)

    # --- Testes da view produto_criar ---

    def test_produto_criar_get_autenticado(self):
        """Verifica se admin autenticado pode acessar o formulário de criação."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('cadastro_produto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_pag.html')

    def test_produto_criar_post_valido(self):
        """Verifica se um produto é criado via POST com dados válidos."""
        self.client.login(username='admin', password='admin123')
        dados = {
            'nome': 'Novo Produto Teste',
            'descricao': 'Descrição do produto criado no teste',
            'preco': '99.90',
            'categoria': self.categoria.pk,
        }
        response = self.client.post(reverse('cadastro_produto'), dados, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Produto.objects.filter(nome='Novo Produto Teste').exists())

    def test_produto_criar_post_sem_autenticacao(self):
        """Verifica que usuário não autenticado recebe 403 ao criar produto."""
        dados = {
            'nome': 'Produto Sem Auth',
            'descricao': 'Teste',
            'preco': '10.00',
            'categoria': self.categoria.pk,
        }
        response = self.client.post(reverse('cadastro_produto'), dados)
        self.assertEqual(response.status_code, 403)

    # --- Testes da view produto_editar ---

    def test_produto_editar_get_autenticado(self):
        """Verifica se admin autenticado pode acessar o formulário de edição."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('produto_editar', args=[self.produto.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro_pag.html')

    def test_produto_editar_post_valido(self):
        """Verifica se um produto é atualizado via POST."""
        self.client.login(username='admin', password='admin123')
        dados = {
            'nome': 'Vela Editada',
            'descricao': 'Descrição editada',
            'preco': '149.90',
            'categoria': self.categoria.pk,
        }
        response = self.client.post(
            reverse('produto_editar', args=[self.produto.id]), dados, follow=True
        )
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Vela Editada')
        self.assertEqual(float(self.produto.preco), 149.90)

    # --- Testes da view produto_remover ---

    def test_produto_remover_autenticado(self):
        """Verifica se admin autenticado pode remover um produto."""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('produto_remover', args=[self.produto.id]), follow=True)
        self.assertFalse(Produto.objects.filter(id=self.produto.id).exists())

    def test_produto_remover_nao_autenticado(self):
        """Verifica que usuário não autenticado recebe 403 ao remover."""
        response = self.client.get(reverse('produto_remover', args=[self.produto.id]))
        self.assertEqual(response.status_code, 403)

    # --- Testes da view login ---

    def test_login_get(self):
        """Verifica se a página de login retorna 200."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_valido(self):
        """Verifica se o login funciona com credenciais corretas."""
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'admin123',
        }, follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_login_post_invalido(self):
        """Verifica se o login falha com credenciais incorretas."""
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'senha_errada',
        })
        self.assertContains(response, 'Credenciais inválidas')

    def test_login_redireciona_se_autenticado(self):
        """Verifica se usuário já logado é redirecionado para o index."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('index'))

    # --- Testes da view cadastro ---

    def test_cadastro_get(self):
        """Verifica se a página de cadastro retorna 200."""
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cadastro.html')

    def test_cadastro_post_valido(self):
        """Verifica se um novo usuário é cadastrado com sucesso."""
        response = self.client.post(reverse('cadastro'), {
            'username': 'novousuario',
            'password1': 'senhaForte123!',
            'password2': 'senhaForte123!',
        }, follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='novousuario').exists())

    def test_cadastro_usuario_grupo_cliente(self):
        """Verifica se o novo usuário é associado ao grupo CLIENTE."""
        self.client.post(reverse('cadastro'), {
            'username': 'novocliente',
            'password1': 'senhaForte123!',
            'password2': 'senhaForte123!',
        })
        usuario = User.objects.get(username='novocliente')
        self.assertTrue(usuario.groups.filter(name='CLIENTE').exists())

    def test_cadastro_redireciona_se_autenticado(self):
        """Verifica se usuário logado é redirecionado para o index."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('cadastro'))
        self.assertRedirects(response, reverse('index'))

    # --- Testes da view desconectar ---

    def test_desconectar(self):
        """Verifica se o logout funciona e redireciona para o index."""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('desconectar'), follow=True)
        self.assertRedirects(response, reverse('index'))
        # Verifica que o usuário não está mais autenticado
        response = self.client.get(reverse('index'))
        self.assertFalse(response.context['user'].is_authenticated)


class URLsTest(TestCase):
    """Testes de sistema para as URLs do projeto."""

    def test_url_index_resolve(self):
        """Verifica se a URL '/' resolve para a view correta."""
        resolver = resolve('/')
        self.assertEqual(resolver.func.__name__, 'listar_produtos')
        self.assertEqual(resolver.url_name, 'index')

    def test_url_login_resolve(self):
        """Verifica se a URL '/login/' resolve para a view correta."""
        resolver = resolve('/login/')
        self.assertEqual(resolver.func.__name__, 'login')

    def test_url_cadastro_resolve(self):
        """Verifica se a URL '/cadastro/' resolve para a view correta."""
        resolver = resolve('/cadastro/')
        self.assertEqual(resolver.func.__name__, 'cadastro')

    def test_url_desconectar_resolve(self):
        """Verifica se a URL '/desconectar/' resolve para a view correta."""
        resolver = resolve('/desconectar/')
        self.assertEqual(resolver.func.__name__, 'desconectar')

    def test_url_produto_criar_resolve(self):
        """Verifica se a URL '/cadastro_produto/' resolve para a view correta."""
        resolver = resolve('/cadastro_produto/')
        self.assertEqual(resolver.func.__name__, 'produto_criar')

    def test_url_admin_resolve(self):
        """Verifica se a URL '/admin/' resolve corretamente."""
        resolver = resolve('/admin/')
        self.assertEqual(resolver.func.__name__, 'index')

    def test_urls_com_id_resolvem(self):
        """Verifica se URLs com parâmetro id resolvem corretamente."""
        resolver_produto = resolve('/produto/1/')
        self.assertEqual(resolver_produto.func.__name__, 'pag_product')
        resolver_editar = resolve('/produto/editar/1/')
        self.assertEqual(resolver_editar.func.__name__, 'produto_editar')
        resolver_remover = resolve('/produto/remover/1/')
        self.assertEqual(resolver_remover.func.__name__, 'produto_remover')

    def test_urls_reverse(self):
        """Verifica se os nomes das URLs geram os caminhos corretos."""
        self.assertEqual(reverse('index'), '/')
        self.assertEqual(reverse('login'), '/login/')
        self.assertEqual(reverse('cadastro'), '/cadastro/')
        self.assertEqual(reverse('desconectar'), '/desconectar/')
        self.assertEqual(reverse('cadastro_produto'), '/cadastro_produto/')
        self.assertEqual(reverse('pag_product', args=[1]), '/produto/1/')
        self.assertEqual(reverse('produto_editar', args=[1]), '/produto/editar/1/')
        self.assertEqual(reverse('produto_remover', args=[1]), '/produto/remover/1/')
