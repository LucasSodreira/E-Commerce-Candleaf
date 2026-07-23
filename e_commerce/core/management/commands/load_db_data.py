# Comando personalizado do Django para carregar dados iniciais no banco
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Carrega dados iniciais no banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write("Carregando dados iniciais...")
        # Lista de grupos que serão criados no banco
        group_names = ["ADMINISTRADOR", "CLIENTE"]

        for group_name in group_names:
            # Cria o grupo se ele não existir
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Grupo '{group_name}' criado com sucesso.")
            else:
                self.stdout.write(f"Grupo '{group_name}' já existe.")

        self.stdout.write("Dados carregados com sucesso.")
