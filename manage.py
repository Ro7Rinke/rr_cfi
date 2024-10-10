#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

def main():
    # Carregue o arquivo .env
    load_dotenv()

    # Obtenha a porta do ambiente
    port = os.getenv('DJANGO_PORT', '8000')  # Valor padrão se a variável não estiver definida

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rr_cfi.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Adiciona a porta ao comando runserver
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] == 'runserver'):
        # Remove qualquer argumento anterior para a porta
        sys.argv = [sys.argv[0], 'runserver', f'0.0.0.0:{port}']

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
