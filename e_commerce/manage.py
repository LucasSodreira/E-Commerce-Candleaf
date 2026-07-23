# Utilitário de linha de comando do Django para tarefas administrativas
import os
import sys

def main():
    # Define qual arquivo de configurações o Django deve usar
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e_commerce.settings')
    try:
        # Tenta importar a função de gerenciamento do Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Verifique se ele está instalado "
            "e disponível no PYTHONPATH. Você esqueceu de ativar um ambiente virtual?"
        ) from exc
    # Executa o comando passado pelo terminal (ex: runserver, migrate, etc.)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
