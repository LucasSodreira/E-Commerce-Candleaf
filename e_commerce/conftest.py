import pytest
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def client(client):
    client.defaults['HTTP_HOST'] = 'testserver'
    return client


@pytest.fixture
def imagem_teste():
    """Cria uma imagem PNG em memória para usar nos testes."""
    img = Image.new('RGB', (100, 100), color='red')
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return SimpleUploadedFile('teste.png', buf.read(), content_type='image/png')


@pytest.fixture
def grupo_admin(db):
    from django.contrib.auth.models import Group
    return Group.objects.create(name='ADMINISTRADOR')


@pytest.fixture
def grupo_cliente(db):
    from django.contrib.auth.models import Group
    return Group.objects.create(name='CLIENTE')


@pytest.fixture
def usuario_admin(db, grupo_admin):
    from core.models import User
    user = User.objects.create_superuser(
        username='admin', password='admin123', email='admin@email.com'
    )
    user.groups.add(grupo_admin)
    return user


@pytest.fixture
def usuario_cliente(db, grupo_cliente):
    from core.models import User
    user = User.objects.create_user(username='cliente', password='cliente123')
    user.groups.add(grupo_cliente)
    return user


@pytest.fixture
def usuario_sem_grupo(db):
    from core.models import User
    return User.objects.create_user(username='solto', password='solto123')


@pytest.fixture
def categoria(db):
    from core.models import Categoria
    return Categoria.objects.create(nome='Velas')


@pytest.fixture
def produto(db, usuario_admin, categoria):
    from core.models import Produto
    return Produto.objects.create(
        nome='Vela Teste',
        descricao='Vela de teste automatizado',
        preco=49.90,
        categoria=categoria,
        user=usuario_admin,
    )
