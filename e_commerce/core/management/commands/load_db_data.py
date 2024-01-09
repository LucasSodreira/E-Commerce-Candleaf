# myapp/management/commands/load_db_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Carrega dados iniciais no banco de dados'

    def handle(self, *args, **kwargs):
        self.stdout.write("Carregando dados iniciais...")
        group_names = ["ADMINISTRADOR", "CLIENTE"]

        for group_name in group_names:
            created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Grupo '{group_name}' criado com sucesso.")
            else:
                self.stdout.write(f"Grupo '{group_name}' já existe.")

        self.stdout.write("Dados carregados com sucesso.")
